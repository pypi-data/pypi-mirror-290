from PySide6.QtWidgets import QApplication

from caqtus.gui.condetrol.device_configuration_editors.sequencer_configuration_editor.channel_output_editor._analog_mapping_node import (
    CalibratedAnalogMappingWidget,
)

if __name__ == "__main__":
    app = QApplication([])

    widget = CalibratedAnalogMappingWidget()
    widget.set_input_units("dB")
    widget.set_data_points(
        [
            (-49.0, 0.5),
            (-36.0, 0.55),
            (-24.0, 0.6),
            (-13.0, 0.65),
            (-6.6, 0.7),
            (-2, 0.8),
            (-1, 0.9),
            (0, 1),
        ]
    )

    widget.show()

    app.exec()
