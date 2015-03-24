import pickle

from pyqtgraph.parametertree import Parameter
import numpy as np


class experiment(Parameter):
    def __init__(self, path=None):

        if path is None:  # If not loading an exeriment from file
            # Build an empty experiment tree
            config = [{'name': 'Name', 'type': 'str', 'value': 'New Experiment'},
                      {'name': 'Detector', 'type': 'str', 'value': 'Unknown'},
                      {'name': 'Pixel Size X', 'type': 'float', 'value': 72e-6, 'siPrefix': True, 'suffix': 'm',
                       'step': 1e-6},
                      {'name': 'Pixel Size Y', 'type': 'float', 'value': 72e-6, 'siPrefix': True, 'suffix': 'm',
                       'step': 1e-6},
                      {'name': 'Center X', 'type': 'int', 'value': 0, 'suffix': ' px'},
                      {'name': 'Center Y', 'type': 'int', 'value': 1210, 'suffix': ' px'},
                      {'name': 'Detector Distance', 'type': 'float', 'value': 1, 'siPrefix': True, 'suffix': 'm',
                       'step': 1e-3},
                      {'name': 'Energy', 'type': 'float', 'value': 9000, 'siPrefix': True, 'suffix': 'eV'},
                      {'name': 'Wavelength', 'type': 'float', 'value': 1, 'siPrefix': True, 'suffix': 'm'},
                      # {'name': 'View Mask', 'type': 'action'},
                      {'name': 'Notes', 'type': 'text', 'value': ''}]
            super(experiment, self).__init__(name='Experiment Properties', type='group', children=config)

            # Wire up the energy and wavelength parameters to fire events on change (so they always match)
            EnergyParam = self.param('Energy')
            WavelengthParam = self.param('Wavelength')
            EnergyParam.sigValueChanged.connect(self.EnergyChanged)
            WavelengthParam.sigValueChanged.connect(self.WavelengthChanged)

            # Start with a null mask
            self.mask = None

            self.EnergyChanged()
        else:
            # Load the experiment from file
            with open(path, 'r') as f:
                self.config = pickle.load(f)

    # Make the mask accessible as a property
    @property
    def mask(self):
        """I'm the 'mask' property."""
        return self._mask

    @mask.setter
    def mask(self, value):
        self._mask = value

    @mask.deleter
    def mask(self):
        del self._mask

    def addtomask(self, maskedarea):
        # If the mask is empty, set the mask to the new masked area
        if self.mask is None:
            self.mask = maskedarea.astype(np.int)
        else:  # Otherwise, bitwise or it with the current mask
            # print(self.experiment.mask,maskedarea)
            self.mask = np.bitwise_or(self.mask, maskedarea.astype(np.int))


    def EnergyChanged(self):
        # Make Energy and Wavelength match
        self.param('Wavelength').setValue(1.239842e-6 / self.param('Energy').value(),
                                          blockSignal=self.WavelengthChanged)

    def WavelengthChanged(self):
        # Make Energy and Wavelength match
        self.param('Energy').setValue(1.239842e-6 / self.param('Wavelength').value(), blockSignal=self.EnergyChanged)

    def save(self):
        # Save the experiment .....
        path = '.emptyexperiment.json'
        with open(self.getvalue('Name') + '.json', 'w') as f:
            pickle.dump(self.saveState(), f)

    def getvalue(self, name):
        # Return the value of the named child
        return self.child(name).value()

    def setValue(self, name, value):
        # Set the value of the named child
        self.child(name).setValue(value)


    def edit(self):
        pass



        # edit the data
        # config['key3'] = 'value3'

        #write it back to the file
        #with open('config.json', 'w') as f:
        #    json.dump(config, f)









