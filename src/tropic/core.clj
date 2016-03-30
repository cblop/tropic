(ns tropic.core
  (:require [me.raynes.conch :refer [programs with-programs let-programs] :as sh]
            [tropic.instal :refer [instal-file]]
            [tropic.text-parser :refer [observe]])
  (:gen-class))

(programs python clingo)

(def output-file (atom ""))
(def inst (atom "starwars"))

(defn show-message []
  (do
    (print "\nWelcome to the land of adventure!\n\n> ")
    (flush)))

(defn process-events [input evs]
  (let [new-ev (observe input @inst (count evs))]
    (spit "resources/query.lp" (str new-ev "\n") :append true)))

(defn get-input []
  (loop [input (read-line) acc []]
    (if (= "quit" input) (println "\nGoodbye!\n")
        (do
          (process-events input acc)
          (print "> ")
          (flush)
          (recur (read-line) (conj acc input)))
      ))
  )

(defn output-file-name [name]
  (-> name
      (clojure.string/split #"\.")
      (first)
      (str ".ial")))

(defn -main [& args]
  (if-not (= (count args) 1) (println "Usage: tropical <STORY_FILE>.story")
    (do
      (spit "resources/query.lp" "")
      (reset! output-file (output-file-name (first args)))
      (instal-file (first args) @output-file)
      (show-message)
      (get-input))))

