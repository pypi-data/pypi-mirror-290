# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import logging
from functools import partial
from typing import Optional

from superset import security_manager
from superset.commands.base import BaseCommand
from superset.commands.report.exceptions import (
    ReportScheduleDeleteFailedError,
    ReportScheduleForbiddenError,
    ReportScheduleNotFoundError,
)
from superset.daos.report import ReportScheduleDAO
from superset.exceptions import SupersetSecurityException
from superset.reports.models import ReportSchedule
from superset.utils.decorators import on_error, transaction

logger = logging.getLogger(__name__)


class DeleteReportScheduleCommand(BaseCommand):
    def __init__(self, model_ids: list[int]):
        self._model_ids = model_ids
        self._models: Optional[list[ReportSchedule]] = None

    @transaction(on_error=partial(on_error, reraise=ReportScheduleDeleteFailedError))
    def run(self) -> None:
        self.validate()
        assert self._models
        ReportScheduleDAO.delete(self._models)

    def validate(self) -> None:
        # Validate/populate model exists
        self._models = ReportScheduleDAO.find_by_ids(self._model_ids)
        if not self._models or len(self._models) != len(self._model_ids):
            raise ReportScheduleNotFoundError()

        # Check ownership
        for model in self._models:
            try:
                security_manager.raise_for_ownership(model)
            except SupersetSecurityException as ex:
                raise ReportScheduleForbiddenError() from ex
