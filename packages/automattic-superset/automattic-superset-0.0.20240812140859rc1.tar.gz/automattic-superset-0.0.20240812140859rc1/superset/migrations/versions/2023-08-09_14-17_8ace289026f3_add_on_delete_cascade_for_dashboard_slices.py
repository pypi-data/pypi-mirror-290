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
"""add on delete cascade for dashboard_slices

Revision ID: 8ace289026f3
Revises: 2e826adca42c
Create Date: 2023-08-09 14:17:53.326191

"""

# revision identifiers, used by Alembic.
revision = "8ace289026f3"
down_revision = "2e826adca42c"


from superset.migrations.shared.constraints import ForeignKey, redefine  # noqa: E402

foreign_keys = [
    ForeignKey(
        table="dashboard_slices",
        referent_table="dashboards",
        local_cols=["dashboard_id"],
        remote_cols=["id"],
    ),
    ForeignKey(
        table="dashboard_slices",
        referent_table="slices",
        local_cols=["slice_id"],
        remote_cols=["id"],
    ),
]


def upgrade():
    for foreign_key in foreign_keys:
        redefine(foreign_key, on_delete="CASCADE")


def downgrade():
    for foreign_key in foreign_keys:
        redefine(foreign_key)
