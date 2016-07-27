(ns tropic.core
  (:require [me.raynes.conch :refer [programs with-programs let-programs] :as sh]
            [tropic.instal :refer [instal-file]]
            [clojure.tools.cli :refer [parse-opts]]
            [clojure.string :as string]
            [tropic.solver :refer [make-cmd]]
            ;; [tropic.text-parser :refer [observe trace-to-prose]]
            )
  (:gen-class))

(def cli-options
  [["-o" "--output FOLDER" "Name of folder to output .ial files to"
    :id :output
    :default "output"
    ]
   ;; ["-i" "--instal" "Run instal to compile ASP .lp files"
   ;;  :id :instal
   ;;  ]
   ["-c" "--chars CHARS" "File with character definitions"
    :id :chars
    ]
   ["-t" "--types OBJECTS" "File with object definitions"
    :id :objs
    ]
   ["-l" "--locations PLACES" "File with place definitions"
    :id :places
    ]
   ["-p" "--player PLAYER" "Name of the player character"
    :id :player
    ]
   ;; A boolean option defaulting to nil
   ["-h" "--help"]])

(defn usage [options-summary]
  (->> ["Compiles trope descriptions to .ial instution files."
        ""
        "Usage: tropical [options] trope_file ..."
        ""
        "Options:"
        options-summary
        ]
       (string/join \newline)))

(defn error-msg [errors]
  (str "The following errors occurred while parsing your command:\n\n"
       (string/join \newline errors)))

(defn exit [status msg]
  (println msg)
  (System/exit status))

(defn -main [& args]
  (let [{:keys [options arguments errors summary]} (parse-opts args cli-options)]
    ;; Handle help and error conditions
    (do
      (cond
        (:help options) (exit 0 (usage summary))
        (not (> (count arguments) 0)) (exit 1 (usage summary))
        errors (exit 1 (error-msg errors)))
      ;; Execute program with options
      (make-cmd arguments (:chars options) (:objs options) (:places options) (:output options) (:player options))
      (exit 0 "")
      )))

