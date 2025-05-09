# $R_X$ efficiencies

Project used to calculate efficiencies for different simulated datasets

## Geometric acceptance

This work was done for Run1/2 datasets by [prec_acceptances](https://gitlab.cern.ch/r_k/prec_acceptances/-/tree/master?ref_type=heads)
and that code has been transferred and upgraded in this project.

### Making ntuples

The geometric acceptance should be calculated using [rapidsim](https://github.com/gcowan/RapidSim)
given that:

1. Accessing the generator tables is not trivial.
1. Using RapidSim is trivial.
1. One might need special definitions for the acceptance and having the ntuples with the
decay product values offers higher flexibility.

More on how to install and configure rapidsim [here](doc/rapidsim.md).

To create the ntuples with the decays, do:

```bash
create_rapidsim_ntuples -n 100000 -o /some/path/to/rapidsim/ntuples
```

where the utility will pick up every decay configuration in the `$RAPIDSIM_CONFIG` directory and 

- Create the respective ntuple with the logfile and some histogram file and with 100K entries.
- Make the output path if not found and send the outputs there.

### Measuring acceptances from them

This can be done with the `AcceptanceCalculator` class as shown below:

```python
from rx_efficiencies.acceptance_calculator import AcceptanceCalculator

obj=AcceptanceCalculator(rdf=rdf)
obj.plot_dir     = '/optional/path/where/diagnostic/plots/are/saved'
acc_phy, acc_lhc = obj.get_acceptances()
```

where `acc_phy` is the physical acceptance and `acc_lhc` is the LHC one:

`Physical Acceptance`: The probability that the detector will see the reconstructed candidate. E.g. for $B_s\to\phi(\to KK)ee$ decays reconstructed as
$B^+\to K^+ee$, the decay counts as in acceptance, even if $K^-$ is not in acceptance.
`LHC acceptance`: What the _generator tables_ provide. All the decay products have to be in the acceptance.

These acceptances can be calculated all at once with:

```bash
calculate_acceptances -v v1
```

which will make the `JSON`, `TEX` and `PNG` files with the acceptances, the tables for the note/paper and the plots.

### Reading acceptances

This is done with the `AcceptanceReader` class with:

```python
from rx_efficiencies.acceptance_reader import AcceptanceReader

obj=AcceptanceReader(year=year, proc=process)
acc=obj.read()
```

## Acceptance, Reconstruction and selection efficiencies

The product of these efficiencies can be obtained by dividing:

`Numerator:` The number of entries in the `DecayTree` after the full selection
`Denominator:` The number of entries in the `MCDecayTree` from the same files.

And multiplying the ratio by the acceptance from RapidSim. This is done by running:

```python
from rx_efficiencies.efficiency_calculator import EfficiencyCalculator

# q2 bin in low, central, high
obj         = EfficiencyCalculator(q2bin='central')
# The plots in this directory show the product of reconstruction and selection efficiencies.
# The YAML files include also the acceptances.
obj.out_dir = '/path/to/validation/directory'
df          = obj.get_stats()
```
which provides a dataframe with the passed and total yields. These yields are not weighted.
