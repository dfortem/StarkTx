#  Copyright 2022 Token Flow Insights
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
#  OF ANY KIND, either express or implied.
#
#  See the License for the specific language governing permissions and limitations
#  under the License.
#
#  The product contains trademarks and other branding elements of Token Flow Insights SA
#  which are not licensed under the Apache 2.0 license. When using or reproducing the code,
#  please remove the trademark and/or other branding elements.
#

from enum import Enum, EnumMeta


class MyEnumMeta(EnumMeta):
    def __contains__(cls, item):
        return item in [k for k in cls.__members__.keys()]


class SequencerStatus(Enum, metaclass=MyEnumMeta):
    NOT_RECEIVED = False, 404
    ACCEPTED_ON_L2 = True, 200
