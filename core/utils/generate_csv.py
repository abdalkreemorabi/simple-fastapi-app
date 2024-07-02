from io import StringIO

import pandas as pd

from core.utils.custom_logger import logger


def sync_generate_csv_report(candidates):
    """
    Generate CSV report from candidates data
    """

    logger.info("Generating CSV report")
    df = pd.DataFrame(candidates)
    csv_data = StringIO()
    df.to_csv(csv_data, index=False)
    csv_data.seek(0)
    logger.info("CSV report generated successfully")
    return csv_data.getvalue()
