(defproject tropic "0.1.0-SNAPSHOT"
  :description "FIXME: write description"
  :url "http://example.com/FIXME"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :dependencies [[org.clojure/clojure "1.6.0"]
                 [instaparse "1.4.1"]
                 [rhizome "0.2.5"]
                 [enlive "1.1.6"]
                 [org.clojure/math.combinatorics "0.1.1"]
                 [damionjunk/nlp  "0.3.0"]
                 [me.raynes/conch "0.8.0"]
                 [org.clojure/tools.cli "0.3.5"]
                 ;; [lingo "0.2.0"o
                 [com.rpl/specter "0.9.0"]]
  :resource-paths ["lib/simplenlg-v4.4.3.jar"]
  :aot [tropic.core]
  :main tropic.core)
