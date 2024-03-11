import sys
import traceback
import json
import logging

import numpy as np
import pandas as pd
import lightgbm as lgb
import structlog
from sagemaker_inference import content_types, decoder, encoder


def add_log_info(logger, method_name, event_dict):
    frame = sys._getframe(5)
    event_dict['code'] = frame.f_code.co_filename  # 実行ファイル名を追加
    event_dict['line'] = frame.f_lineno  # log実行行番号を追加
    if event_dict.get('exc_info'):
        # 例外情報を追加
        exception_formatted = [line.strip() for line in traceback.format_exc().splitlines()]
        event_dict['exception'] = exception_formatted
    return event_dict


structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        add_log_info,
        structlog.processors.JSONRenderer(ensure_ascii=False),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)
logger = structlog.get_logger()


def model_fn(model_dir: str, context=None) -> object:
    try:
        logger.info("Model loading")
        model = lgb.Booster(model_file=f'{model_dir}/model.lgb')
        logger.info("Model loaded successfully.")
        return model
    except Exception as e:
        logger.error("Error in model_fn", exc_info=e)
        raise


def input_fn(input_data: str | bytes, content_type: str, context=None) -> pd.DataFrame:
    try:
        if content_type != 'application/json':
            raise ValueError(f"Unsupported content type: {content_type}")
        input_str = input_data.decode('utf-8') if isinstance(input_data, bytes) else input_data
        input_obj = json.loads(input_str)
        logger.info('Receive a request', input_data=input_obj)
        data = pd.DataFrame(input_obj)
        return data
    except Exception as e:
        logger.error("Error in input_fn", exc_info=e)
        raise


def predict_fn(data: pd.DataFrame, model: object, context=None) -> np.ndarray:
    try:
        return model.predict(data)
    except Exception as e:
        logger.error("Error in predict_fn", exc_info=e)
        raise


def output_fn(prediction: np.ndarray, accept: str, context=None) -> object:
    try:
        if accept == "application/json":
            return json.dumps(prediction.tolist())
        raise ValueError(f"Unsupported accept type: {accept}")
    except Exception as e:
        logger.error(f"Error in output_fn", exc_info=e)
        raise
