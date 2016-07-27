# Tropic

We're using Clojure's [instaparse](https://github.com/Engelberg/instaparse) library to create a parser that reads in near natural-language descriptions of tropes with a syntax similar to that of [Inform 7](http://inform7.com).

The parser is based on the BNF syntax listed [here](http://inform7.com/learn/man/WI_19_7.html#e41).

## Usage

java -jar target/tropic-0.1.0-SNAPSHOT-standalone.jar [options] trope-file1 trope-file2 ...

Options:
  -o, --output FOLDER     output  Name of folder to output .ial files to
  -c, --chars CHARS               File with character definitions
  -t, --types OBJECTS             File with object definitions
  -l, --locations PLACES          File with place definitions
  -p, --player PLAYER             Name of the player character
  -h, --help
  
_poltest.sh_ is an example script that compiles policy files. Look at how it's called, run it, and examine the output in the "resources/poltest" directory. It uses the policies in the "policies" directory and agents/objects/places in the "things" directory.

## Compiling

Precompiled jars are in the _target_ folder, but to compile for yourself run:

```
lein uberjar
```

Or to run without compilation:

```
lein run [options] trope-file1 trope-file2 ...
```

## License

Copyright © 2015 Matt Thompson

Distributed under the Eclipse Public License either version 1.0 or (at
your option) any later version.
