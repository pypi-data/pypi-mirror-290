# Copyright (c) 2021-2024  The University of Texas Southwestern Medical Center.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted for academic and research use only (subject to the
# limitations in the disclaimer below) provided that the following conditions are met:

#      * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.

#      * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.

#      * Neither the name of the copyright holders nor the names of its
#      contributors may be used to endorse or promote products derived from this
#      software without specific prior written permission.

# NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY
# THIS LICENSE. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Standard Imports

# Third party imports

# Local Imports
from navigate.model.devices.stages.stage_base import StageBase

class StageDevice(StageBase):
    """MMCore Stage Device Class."""
    def __init__(self, microscope_name, device_connection, configuration, device_id=0):
        """Initialize the MMCore Stage Device Class.

        Parameters
        ----------
        microscope_name : str
            Name of microscope in configuration
        device_connection : object
            Hardware device to connect to
        configuration
            Global configuration of the microscope
        device_id : int
            Device ID
        """
        super().__init__(microscope_name, device_connection, configuration, device_id)

        #: Object: MMCore device connection
        self.mmcore = device_connection

        if not self.axes_mapping:
            #: dict: Mapping of MMCore stage axes to x, y, z, theta, f.
            self.axes_mapping = {
                axis: axis for axis in self.axes
            }

        # make sure only mapping to x, y, or z
        for axis, v in self.axes_mapping.items():
            if v.lower() == "z":
                self.axes_mapping[axis] = "z"
                if not self.mmcore.getFocusDevice():
                    raise Exception(
                        f"MMCore stage {axis} should be the Focus stage! "
                        "Please set it in MMCore and update the cfg file!"
                    )
            elif v.lower() == "x" or v.lower() == "y":
                self.axes_mapping[axis] = v.lower()
                if not self.mmcore.getXYStageDevice():
                    raise Exception(
                        f"MMCore stage {axis} should be the XY stage! "
                        "Please set it in MMCore and update the cfg file!"
                    )
            else:
                print(f"Warning: MMCore stage {axis} is mapped to an invalid "
                      f"axis! Only x, y or z works!")
                self.axes_mapping.pop(axis)


    def report_position(self):
        """Reports the position for all axes, and create position dictionary.

        Positions from Physik Instrumente device are in millimeters

        Returns
        -------
        position_dict : dict
            Dictionary containing the position of all axes
        """
        for axis, m_axis in self.axes_mapping.items():
            if m_axis == "z":
                pos = self.mmcore.getPosition()
                setattr(self, f"{axis}_pos", pos)
            elif m_axis == "x":
                pos = self.mmcore.getXPosition()
                setattr(self, f"{axis}_pos", pos)
            elif m_axis == "y":
                pos = self.mmcore.getYPosition()
                setattr(self, f"{axis}_pos", pos)

        return self.get_position_dict()

    def move_axis_absolute(self, axis, abs_pos, wait_until_done=True):
        """Move stage along a single axis.

        Parameters
        ----------
        axis : str
            An axis. For example, 'x', 'y', 'z', 'f', 'theta'.
        abs_pos : float
            Absolute position value
        wait_until_done : bool
            Block until stage has moved to its new spot.

        Returns
        -------
        bool
            Was the move successful?
        """
        if axis not in self.axes_mapping:
            return False

        axis_abs = self.get_abs_position(axis, abs_pos)
        if axis_abs == -1e50:
            return False
        
        try:
            if self.axes_mapping[axis] == "z":
                self.mmcore.setPosition(axis_abs)
            elif self.axes_mapping[axis] == "y":
                x_pos = self.mmcore.getXPosition()
                self.mmcore.setXYPosition(x_pos, axis_abs)
            elif self.axes_mapping[axis] == "x":
                y_pos = self.mmcore.getYPosition()
                self.mmcore.setXYPosition(axis_abs, y_pos)
        except Exception:
            print(f"Error: MMCore stage move to {abs_pos} failed!")
            return False
    
        return True

    def move_absolute(self, move_dictionary, wait_until_done=True):
        """Move Absolute Method.

        XYZF Values are converted to millimeters for PI API.
        Theta Values are not converted.

        Parameters
        ----------
        move_dictionary : dict
            A dictionary of values required for movement. Includes 'x_abs', etc. for one
            or more axes. Expect values in micrometers, except for theta, which is
            in degrees.
        wait_until_done : bool
            Block until stage has moved to its new spot.

        Returns
        -------
        bool
            Was the move successful?
        """
        abs_pos_dict = self.verify_abs_position(move_dictionary)
        if not abs_pos_dict:
            return False
        
        result = True
        axis_x, axis_y = None, None
        for axis in abs_pos_dict:
            if self.axes_mapping[axis] == "z":
                try:
                    self.mmcore.setPosition(abs_pos_dict[axis])
                except Exception:
                    print(f"Warning: moving MMCore stage{axis} failed!")
                    result = False
            elif self.axes_mapping[axis] == "x":
                axis_x = axis
            elif self.axes_mapping[axis] == "y":
                axis_y = axis
        if axis_x and axis_y:
            try:
                self.mmcore.setXYPosition(abs_pos_dict[axis_x], abs_pos_dict[axis_y])
            except Exception:
                print(f"Warning: moving MMCore stage({axis_x}, {axis_y}) failed!")
                result = False
        elif axis_x:
            result = result and self.move_axis_absolute(axis_x, abs_pos_dict[axis_x])
        elif axis_y:
            result = result and self.move_axis_absolute(axis_y, abs_pos_dict[axis_y])

        return result


    def stop(self):
        """Stop all stage movement abruptly."""

        print("Warning: MMCore stage may not support stopping stage!")
        for _, axis in self.axes_mapping.items():
            if axis == "z":
                stage_label = self.mmcore.getFocusDevice()
            else:
                stage_label = self.mmcore.getXYStageDevice()

            try:
                self.mmcore.stopStageSequence(stage_label)
            except Exception:
                pass

