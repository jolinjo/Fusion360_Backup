# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Copyright (c) 2020 by Patrick Rainsberry.                                   ~
#  Modified by Jason.Lin                                                       ~
#  :license: Apache2, see LICENSE for more details.                            ~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  CloseAllCommand.py                                                            ~
#  This file is a component of BackupTool (Fusion360Tools).                       ~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import apper
from apper import AppObjects


class CloseAllCommand(apper.Fusion360CommandBase):

    def on_execute(self, command, inputs, args, input_values):
        ao = AppObjects()
        document = ao.document

        if document.isSaved:
            document.close(False)

            close_command = ao.ui.commandDefinitions.itemById(self.cmd_id)
            close_command.execute()

