import requests
import pandas as pd
from datetime import datetime
import pytz
import os
import logging

logger = logging.getLogger(__name__)

SERVICENOW_DISPLAY_VALUE = 'display_value'
FIELD_NAME_MAPPING = 'fieldname_mapping'
FIELD_VALUE_MAPPING = 'fieldvalue_mapping'
FIELD_VALUE_REGEX = 'regex'
FIELD_VALUE_REPLACE = 'replace'
FIELD_STATIC_VALUE = 'static_fieldvalue'
CLEAR_ATTRIBUTE_FROM_ALL = 'clear_attribute'
DEDUP = 'deduplicate'
DEDUP_ON_FIELDS = 'on_fields'
DEDUP_PRECEDENCE = 'precedence'
DEDUP_PRECEDENCE_OPERATIONS = ['EQUALS', 'MAX', 'MIN']

class SnowDataSourceException(Exception):
    pass

def get_resources_df(job):
    instance_url = os.getenv("SERVICENOW_URL") or job['source']['servicenow']['instance_url']
    url = instance_url + f"/api/now/table/{job['source']['servicenow']['table']}"

    user = os.getenv("SERVICENOW_USER") or job['source']['servicenow']['auth']['username']
    password = os.getenv("SERVICENOW_PASSWORD") or job['source']['servicenow']['auth']['password']
    auth = requests.auth.HTTPBasicAuth(user, password)
    qstrings = {}
    for k, v in job['source']['servicenow']['query_parameters'].items():
        qstrings[f'sysparm_{k}'] = v
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.get(url=url, auth=auth, params=qstrings, headers=headers)
    try:
        responsedict = response.json()
    except Exception as e:
        msg = f'Failed to retrieve records from ServiceNow datasource: {e}'
        raise SnowDataSourceException(msg)
    records = responsedict.get('result', [])
    processed_recs = []
    for record in records:
        newrec = {}
        for key,value in record.items():
            if isinstance(value, dict) and SERVICENOW_DISPLAY_VALUE in value:
                newrec[key] = value[SERVICENOW_DISPLAY_VALUE]
            else:
                newrec[key] = value
        processed_recs.append(newrec)

    df = pd.DataFrame(processed_recs)

    if FIELD_NAME_MAPPING in job and isinstance(job[FIELD_NAME_MAPPING], dict):
        for old, new in job[FIELD_NAME_MAPPING].items():
            if old in df.columns:
                df.rename(columns={old: new}, inplace=True)
    

    if FIELD_VALUE_MAPPING in job and isinstance(job[FIELD_VALUE_MAPPING], dict):
        for fieldname, mappings in job[FIELD_VALUE_MAPPING].items():
            if fieldname in df.columns and isinstance(mappings, list):
                for mapping in mappings:
                    if isinstance(mapping, dict) and FIELD_VALUE_REGEX in mapping and FIELD_VALUE_REPLACE in mapping:
                        df[fieldname] = df[fieldname].str.replace(mapping[FIELD_VALUE_REGEX], mapping[FIELD_VALUE_REPLACE], regex=True)
    
    if FIELD_STATIC_VALUE in job and isinstance(job[FIELD_STATIC_VALUE], dict):
        for field, value in job[FIELD_STATIC_VALUE].items():
            if value == 'TIMESTAMPLOCAL()':
                value = str(datetime.now())
            elif value == 'TIMESTAMPUTC()':
                value = str(datetime.now().astimezone(pytz.utc))
            elif value == 'DATELOCAL()':
                value = datetime.now().strftime('%Y-%m-%d')
            elif value == 'DATEUTC()':
                value = datetime.now().astimezone(pytz.utc).strftime('%Y-%m-%d')
            df[field] = value


    if 'exceptions' in job:
        for fieldname, values_to_exclude in job['exceptions'].items():
            df = df[~df[fieldname].isin(values_to_exclude)]

    if CLEAR_ATTRIBUTE_FROM_ALL in job:
            for fieldname in job[CLEAR_ATTRIBUTE_FROM_ALL]:
                df[fieldname] = ''

    if DEDUP in job \
      and DEDUP_ON_FIELDS in job[DEDUP] \
      and DEDUP_PRECEDENCE in job[DEDUP] \
      and type(job[DEDUP][DEDUP_ON_FIELDS]) == list \
      and len(job[DEDUP][DEDUP_ON_FIELDS]) > 0 \
      and type(job[DEDUP][DEDUP_PRECEDENCE]) == list \
      and len(job[DEDUP][DEDUP_PRECEDENCE]) > 0 :
        logger.info(f'Pre-deduplication source record count: {len(df.index)}')
        
        dedup_on_fields = job[DEDUP][DEDUP_ON_FIELDS]
        precedences = job[DEDUP][DEDUP_PRECEDENCE]

        logger.info('Validating job dedup fields')
        if type(dedup_on_fields) == list and len(dedup_on_fields) > 0:
            for field in dedup_on_fields:
                if field not in df.columns:
                    msg = f'Field {field} is specified in deduplicate.on_fields in the job file, but is not a valid field name.  In the job file check source.servicenow.query_parameters.fields and fieldname_mapping.'
                    logger.error(msg)
                    raise SnowDataSourceException(msg)
        else:
            msg = f'In the job file, deduplicate.on_fields must contain a list of one or more fields to deduplicate on.'
            logger.error(msg)
            raise SnowDataSourceException(msg)
        
        logger.info('Validating job dedup precedences')
        for precedence in precedences:
            if precedence['field'] not in df.columns:
              msg = f'Field {field} is specified in deduplicate.precedence[].field in the job file, but is not a valid field name.  In the job file check source.servicenow.query_parameters.fields and fieldname_mapping.'
              logger.error(msg)
              raise SnowDataSourceException(msg)
            if precedence['operation'] not in DEDUP_PRECEDENCE_OPERATIONS:
                msg = f'Precedence operation "{precedence["operation"]}" is not valid.  Please use one of {", ".join(DEDUP_PRECEDENCE_OPERATIONS)}.'
                logger.error(msg)
                raise SnowDataSourceException(msg)
            if precedence['operation'] == 'EQUALS' and 'value' not in precedence:
                msg = f'Precedence operation "EQUALS" requires a value attribute..'
                logger.error(msg)
                raise SnowDataSourceException(msg)
            
        logger.info('Applying dedup criteria')
        counts = df.groupby(dedup_on_fields).size().reset_index(name='count')
        dups = counts[counts['count'] > 1]

        for idx,dup in dups.iterrows():
            dedup_done = False
            query_str_base = ' & '.join([f'`{key}` == "{val}"' for key,val in dup.drop('count').items()])
            for precedence in precedences:
                if dedup_done:
                    break
                if precedence['operation'] == 'EQUALS':
                    query_str = query_str_base + f' & `{precedence["field"]}` == "{precedence["value"]}"'
                elif precedence['operation'] == 'MAX':
                    maxval = df.query(query_str_base)[precedence["field"]].max()
                    query_str = query_str_base + f' & `{precedence["field"]}` == "{maxval}"'
                elif precedence['operation'] == 'MIN':
                    minval = df.query(query_str_base)[precedence["field"]].min()
                    query_str = query_str_base + f' & `{precedence["field"]}` == "{minval}"'

                match_check_df = df.query(query_str)
                remaining = len(match_check_df.index)
                if remaining == 1:
                    df = df.query(f'not ({query_str_base}) or ({query_str})')
                    dup['count'] = 1
                    dedup_done = True
                elif remaining > 1 and remaining < dup['count']:
                    df = df.query(f'not ({query_str_base}) or ({query_str})')
                    dup['count'] = remaining
            if not dedup_done:
                logger.warn(f'Unable to deduplicate with current job settings: {dup.to_json()}')
        logger.info(f'Post-deduplication source record count: {len(df.index)}')

    return df