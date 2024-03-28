def fourier(filename, fs):
    if filename == "ekg noise.txt":
        data = numpy.loadtxt(filename)
        y = data[:, 1]
    else:
        y = numpy.loadtxt(filename)
    n = len(y)
    Y = numpy.fft.fft(y)
    P2 = numpy.abs(Y)
    P1 = P2[:n // 2 + 1] / n
    P1[1:-1] = 2 * P1[1:-1]
    f = numpy.linspace(0, fs/2, len(P1))
    plot.figure(figsize=(10, 6))
    plot.plot(f, P1)
    plot.title('Widmo amplitudowe sygnału')
    plot.xlabel('Częstotliwość (Hz)')
    plot.ylabel('Amplituda')
    plot.grid(True)
    plot.show()