arglist = getArgument();
args = split(arglist, '#');

print("Opening tif...");
open(args[0]);
print("Downsampling tif...");
run("Size...", "width=512 height=512 depth=511 constrain average interpolation=Bilinear");
print("Converting tif to 8-bit...");
run("8-bit");
print("Convert to mask...")
setOption("BlackBackground", true);
run("Convert to Mask", "method=IsoData background=Dark calculate black");
saveAs("Gif", args[1]);