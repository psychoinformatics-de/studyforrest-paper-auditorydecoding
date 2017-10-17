from mvpa2.suite import LinearCSVMC

#fsel = SensitivityBasedFeatureSelection(
#    OneWayAnova(),
#    FractionTailSelector(
#        1.0,
#        mode='select',
#        tail='upper'))

def fx(target_arg, param=-1):
    return LinearCSVMC(C=param, space=target_arg)
