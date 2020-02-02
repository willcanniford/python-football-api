def printProgressBar(
        iteration,
        total,
        prefix='',
        suffix='',
        decimals=2,
        length=20,
        fill='#',
        printEnd="\r",
        endStatement='Complete'):
    percent_complete = (
        "{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(
        '\r%s |%s| %s%% %s' %
        (prefix,
         bar,
         percent_complete,
         suffix),
        end=printEnd)

    if iteration == total:
        print(endStatement)  # Print end statement when complete