============================
Observational Large Ensemble
============================

This package contains code for creation of an "Observational Large Ensemble" of monthly temperature, precipitation, and sea level pressure.

The approach is based upon modeling each variable as a linear combination of a mean, trend, contribution from large-scale modes of variability, and residual climate noise. The ensemble is created through randomization of the latter two components. The time series of the large-scale modes are randomized through application of the Iterative Amplitude Adjusted Fourier Transform. The climate noise is block bootstrapped in time.

The forced component is estimated using the methodology of Dai et al., 2015, Nature Climate Change. Specifically, the observations are regressed against the time series of the global mean, ensemble mean of each variable. The forced trend for sea level pressure is assumed to be zero.

More complete technical and scientific documentation can be found in McKinnon and Deser, 2018, Journal of Climate. However, there are a small number of changes between the methodology documented in McKinnon and Deser (2018) and this code base, which are not currently published. Specifically:

- The data product is monthly, rather than seasonal.
- The seasonality of ENSO variance is included.
- Rather than creating two orthogonal modes from applying PCA the ENSO and PDO, PDO is orthogonalized with respect to ENSO using the Gram-Schmidt orthogonalization procedure.
- The block boostrap size is estimated using the iterative formula of Wilks (1997), Journal of Climate, rather than fixed at two years.
- The AMV time series is lowpass filtered using a cutoff-frequency of 20 years.

The code is designed to be applied either to gridded observational datasets or to the CESM1-LE, which is used as a testbed for the methodology.

Please contact Karen McKinnon (kmckinnon@ucla.edu) if you are using the code or methods in your work.

* Free software: MIT license

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


UPDATES June 28, 2023
----------
- This version of the Observational Large Ensemble was updated to include the Caribbean Low Level Jet (CLLJ) as a climate predictor.
- This approach was taken specifically for research questions related to Central America, where the CLLJ is an important mechanism that influences climate variability.
- All parameter files used to generate the OLEns in the manuscript are included and listed below:
    1) prec-synth-OLE: params-prec-synth-OLE.py
    2) forced pdsi-synth-OLE: params_forced-pdsi-synth-OLE.py
    3) unforced pdsi-synth-OLE: params-unforced-pdsi-synth-OLE.py
       It is also necessary to comment out the Forced component in the combine_variability function in the model_components.py file for the unforced version to successfully run.

- If you would like to run the test excluding the 2015-2019 precipitation data, but maintaining all possible values for the climate modes, it is necessary to uncomment a few lines in the fit_linear_model and combine_variability functions
in the model_components.py file. The parameter file is: params_obs_pr_2014beta_iaaftAll.py

* This repository maintains the same structure as the original Observational Large Ensemble, but includes an additional folder (FinalFigures) where code to produce figures has been added.
