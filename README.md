# Tropic

We're using Clojure's [instaparse](https://github.com/Engelberg/instaparse) library to create a parser that reads in near natural-language descriptions of tropes with a syntax similar to that of [Inform 7](http://inform7.com).

The parser is based on the BNF syntax listed [here](http://inform7.com/learn/man/WI_19_7.html#e41).

## Usage

As of now, just play around with [core.clj](src/tropic/core.clj). Call the _inform_ function with the string you want to parse, so long as that string is one Inform 7 would recognise.

## License

Copyright © 2015 Matt Thompson

Distributed under the Eclipse Public License either version 1.0 or (at
your option) any later version.
