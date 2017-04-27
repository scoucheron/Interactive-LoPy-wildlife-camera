import machine

def measure():
    numADCreadings = const(100)
    adc = machine.ADC(0)
    adcread = adc.channel(attn=1, pin='P16')
    samplesADC = [0.0]*numADCreadings; meanADC = 0.0
    i = 0
    while (i < numADCreadings):
        adcint = adcread()
        samplesADC[i] = adcint
        meanADC += adcint
        i += 1
    meanADC /= numADCreadings
    varianceADC = 0.0
    for adcint in samplesADC:
        varianceADC += (adcint - meanADC)**2
    varianceADC /= (numADCreadings - 1)
    battery_percent = ((meanADC*1400/4096)/1400)*100
    return battery_percent
