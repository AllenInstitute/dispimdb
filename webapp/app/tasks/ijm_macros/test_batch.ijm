arglist = getArgument();
args = split(arglist, '#');

list = getFileList(args[0])
for (i = 0; i < list.length; i++) {
    start = getTime();
    print("Opening " + list[i] + "...");
    open(args[0] + "/" + list[i]);
    run("Size...", "width=512 height=512 depth=511 constrain average interpolation=Bilinear");
    run("8-bit");
    setOption("BlackBackground", true);
    run("Convert to Mask", "method=IsoData background=Dark calculate black");
    saveAs("Gif", args[1] + "/" + list[i]);
    print(list[i] + " took " + ((getTime()-start) / 1000) + " seconds");
}