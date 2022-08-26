# Synthetix Best Execution Pricing Calibration
 
 Calibrates the parameters ( $\beta$ ) of the function below to fit a specified slippage curve given as an input:

$$
f(x) = \beta_0 + \beta_1 \sqrt x + \beta_2 x + \beta_3 x^2
$$

Then uses that model to produce a on-chain slippage model as described in [SIP-272](https://sips.synthetix.io/sips/sip-272/#abstract) . 
f(x) is first integrated, denoted `F(x)`, then transformed into `G(x)` represeting the slippage model that accepts a given amount of cumulative volume and gives back the necessary slippage amount in bp.

$$
F(x) = \beta_0  x + \frac{2}{3} \beta_1 x^{3/2} + \frac{1}{2}  \beta_2 x^2 + \frac{1}{3}  \beta_3 x^3 \\

G(x) = 2  F(x) / x  \\
     = 2  ( \beta_0  + \frac{2}{3} \beta_1 \sqrt x + \frac{1}{2}  \beta_2 x + \frac{1}{3}  \beta_3 x^2 ) \\
     = 2\beta_0  + \frac{4}{3} \beta_1 \sqrt x +  \beta_2 x + \frac{2}{3}  \beta_3 x^2 )
$$




## To Setup

### CREATE FOLDER FOR A PROJECT
```
$ mkdir sip_272
$ cd sip_272
$ git clone git@github.com:kaleb-keny/synthetix_slippage_calibration_sip_272.git
```

### Incorporate Input Data

The input csv file under [here](https://github.com/kaleb-keny/synthetix_slippage_calibration_sip_272/tree/main/input) takes the following form:

| trade_amount 	| uni_slippage 	| cex_slippage 	|
|--------------	|--------------	|--------------	|
| 25000.00     	| 0.00         	| 0.00         	|
| 75000.00     	| 0.67         	| 0.96         	|
| 125000.00    	| 1.34         	| 1.80         	|
| 175000.00    	| 2.02         	| 2.14         	|
| 225000.00    	| 2.69         	| 2.38         	|
| 275000.00    	| 3.37         	| 2.96         	|
| 325000.00    	| 4.03         	| 3.16         	|
| 375000.00    	| 4.72         	| 3.51         	|
| 425000.00    	| 5.37         	| 3.78         	|
| 475000.00    	| 6.07         	| 4.09         	|

- `trade_amount` represents the amount traded in a given direction
- `uni_slippage` and `cex_slippage` represents the slippage in bp incurred from executing a given trade

### Install docker
Refer to [docker](https://docs.docker.com/get-docker/) documentation for installation of docker

### Launch model
```
$ docker build --tag sip_272 .
$ docker run -v$(pwd)/output:/app/output --name sip_272 sip_272
```

## Output
The output folder consists of 3 files
- [The function coefficients calibrated](https://github.com/kaleb-keny/synthetix_slippage_calibration_sip_272/blob/main/output/model.json)
- [The numerical output of applying the end-state models on `trade_amount`](https://github.com/kaleb-keny/synthetix_slippage_calibration_sip_272/blob/main/output/model_slippage.csv)
- [A graphical display of the fits](https://github.com/kaleb-keny/synthetix_slippage_calibration_sip_272/blob/main/output/slippage.jpeg)


## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).