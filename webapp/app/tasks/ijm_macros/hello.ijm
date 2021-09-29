arglist = getArgument();
args = split(arglist, '#');
print("Running analysis with arguments:");
print(args.length);
for (i = 0; i < args.length; i++)
    print(args[i]);