(ns tropic.solver
  (:require
   [tropic.instal :refer [event-name instal-file bridge-file]]
   [clojure.java.io :as io]
   [tropic.gen :refer [make-map make-inst-map]]
   [tropic.parser :refer [parse-trope parse-char parse-object parse-place]]
   [tropic.text-parser :refer [query-parse answer-set-to-map]]
   [clojure.java.shell :refer [sh]]
   [me.raynes.conch :refer [programs with-programs let-programs] :as sh]
   [clojure.string :as str]))

(programs python2 clingo)

(def ARCH (if (= (System/getProperty "os.name") "Mac OS X") "instal"
               (if (= (System/getProperty "os.arch") "amd64") "instal-linux" "instal-arm")))

(defn random-character []
  "Random Character")

(defn random-object []
  "Random Object")

(defn random-place []
  "Random Place")

(defn stringer [item]
  (reduce str (interpose " " (map #(if (nil? %) "random" (event-name %)) item))))

(defn make-domain [hmap id]
  (let [tropes (:tropes hmap)
        tropenames (str "tropeBridge " (stringer (vec (set (map :label tropes)))))
        characters (:characters hmap)
        charnames (stringer (map :label characters))
        roles (stringer (vec (set (map :role characters))))
        places (:places hmap)
        placenames (stringer (map :label places))
        locations (stringer (vec (set (map :location places))))
        objects (conj (:objects hmap))
        objectnames (stringer (map :label objects))
        types (stringer (vec (set (map :type objects))))
        phases (reduce str (interpose " " ["inactive" "done" "phaseA" "phaseB" "phaseC" "phaseD" "phaseE" "phaseF" "phaseG" "phaseH" "phaseI" "phaseJ"]))
        strings ["Identity: id" (if (seq tropes) (str "\nTrope: " tropenames)) "\nPhase: " phases (str "\nAgent: " (if (seq charnames) charnames "noagent")) (str "\nRole: " (if (seq roles) roles "nobody")) (str "\nPlace: " (if (seq locations) locations "noplace")) (str "\nPlaceName: " (if (seq placenames) placenames "nowhere")) (str "\nObject: " (if (seq types) types "noobject")) (str "\nObjectName: " (if (seq objectnames) objectnames "nothing"))]
        final (reduce str strings)
        ]
    (do (spit (str "resources/" id "/domain-" id ".idc") final)
        {:text final})
    ))

;; (defn make-bridge [hmap id]
;;   (dorun (map #(bridge-file (assoc hmap :tropes [%]) (str "resources/" id "-" (event-name (:label %)) ".ial")) (:tropes hmap))))

(defn make-instal [hmap id]
  (dorun (map #(instal-file (assoc hmap :tropes [%]) (:tropes hmap) (str "resources/" id "/" id "-" (event-name (:label %)) ".ial")) (:tropes hmap))))

(defn make-bridge [hmap id]
  (bridge-file (:tropes hmap) (str "resources/" id "/" id "-bridge.ial")))

(defn make-query [events id]
  (spit (str "resources/" id "/query-" id ".iaq") ""))

(defn clean-up [id]
  (do
    (io/delete-file (str "resources/domain-" id ".idc"))
    (io/delete-file (str "resources/story-" id ".ial"))
    (io/delete-file (str "resources/temp-" id ".lp"))
    (io/delete-file (str "resources/query-" id ".lp"))
    (io/delete-file (str "resources/output-" id ".lp"))
    true
    ))


(defn delete-traces [id]
  (let [tracedir (clojure.java.io/file (str "resources/" id "/traces"))
        traces (filter #(.isFile %) (file-seq tracedir))]
    (do
      (doseq [t traces]
        (io/delete-file t))
      true)))

(defn delete-json [id]
  (let [tracedir (clojure.java.io/file (str "resources/" id "/json"))
        traces (filter #(.isFile %) (file-seq tracedir))]
    (do
      (doseq [t traces]
        (io/delete-file t))
      true)))


(defn make-story [hmap id lookahead]
  (let [trps (map :label (:tropes hmap))
        ials (map #(str "resources/" id "/" id "-" (event-name %) ".ial") trps)
        debug (str "resources/" id "/debug-" id ".lp")
        debug2 (str "resources/" id "/debug2-" id ".lp")
        constraint "resources/constraint.lp"
        ]
   (do
     (delete-json id)
     (delete-traces id)
     (println (str "Architecture: " ARCH))
     (.mkdir (java.io.File. (str "resources/" id)))
     (.mkdir (java.io.File. (str "resources/" id "/json")))
     (.mkdir (java.io.File. (str "resources/" id "/traces")))
     (make-domain hmap id)
     (make-instal hmap id)
     (make-bridge hmap id)
     (make-query [] id)
     ;; (let [output (apply sh (concat ["python3" (str ARCH "/instalquery.py") "-v" "-i"] (conj ials constraint) (if (> (count ials) 1) ["-b" (str "resources/" id "/" id "-bridge.ial")]) [(str "-l " lookahead) "-n 0" "-x" (str "resources/" id "/traces/trace-" id "-.lp") "-d" (str "resources/" id "/domain-" id ".idc")]))
     (let [output (apply sh (concat ["python3" (str ARCH "/instalquery.py") "-v" "-i"] (conj ials constraint) (if (> (count ials) 1) ["-b" (str "resources/" id "/" id "-bridge.ial")]) [(str "-l " lookahead) "-n 0" "-j" (str "resources/" id "/json") "-d" (str "resources/" id "/domain-" id ".idc")]))
           t-output (apply sh ["python3" (str ARCH "/instaltrace.py") "-j" (str "resources/" id "/json/") "-x" (str "resources/" id "/traces")])
           tracedir (clojure.java.io/file (str "resources/" id "/traces"))
           traces (filter #(.isFile %) (file-seq tracedir))
           sets (for [t traces]
                  (answer-set-to-map (slurp t)))
           ]
       (do
         (spit debug output)
         (spit debug2 t-output)
         (spit (str "resources/" id "/sets-" id ".edn") (prn-str sets))
         (spit (str "resources/" id "/output-" id ".lp") output)
         ;; (clean-up id)
         {:id id
          :sets sets
          :text "Welcome to the world of adventure!"}))
     )))

(defn event-to-text [{:keys [player verb object-a object-b]}]
  (str "observed(" verb "(" player (if object-a (str "," object-a (if object-b (str "," object-b)) ")")) ")"))

(defn events-to-text[events]
  (apply str (interpose "\n" (map event-to-text events))))


(defn solve-story [id tropes events lookahead]
  (let [trps (map :label tropes)
        ials (map #(str "resources/" id "/" id "-" (event-name %) ".ial") trps)
        domain (str "resources/" id "/domain-" id ".idc")
        temp (str "resources/" id "/temp-" id ".lp")
        query (str "resources/" id "/query-" id ".iaq")
        bridge (str "resources/" id "/" id "-bridge.ial")
        outfile (str "resources/" id "/output-" id ".json")
        debug (str "resources/" id "/debug-" id ".lp")
        constraint "resources/constraint.lp"
        ]
    (do
      (delete-traces id)
      (delete-json id)
      (if (seq events)
        (spit query (events-to-text events) :append false))
      ;; (let [output (apply sh (concat ["python2" "instal/instalsolve.py" "-v" "-i"] ials ["-d" domain "-q" query]))]
      ;; (let [output (apply sh (concat ["python2" "instal-linux/instalquery.py" "-v" "-i"] (conj ials (str "resources/" id "/constraint.lp")) ["-l 1" "-n 0" "-x" (str "resources/" id "/traces/trace-" id "-.lp") "-b" bridge "-d" domain] (if events ["-q" query])))]
      ;; (let [output (apply sh (concat ["python2" (str ARCH "/instalquery.py") "-v" "-i"] (conj ials constraint) (if (> (count ials) 1) ["-b" bridge]) [(str "-l " lookahead) "-o /tmp/out/" "-n 0" "-x" (str "resources/" id "/traces/trace-" id "-.lp") "-d" domain] (if events ["-q" query])))
      (let [output (apply sh (concat ["python3" (str ARCH "/instalquery.py") "-v" "-i"] (conj ials constraint) (if (> (count ials) 1) ["-b" (str "resources/" id "/" id "-bridge.ial")]) [(str "-l " lookahead) "-n 0" "-j" (str "resources/" id "/json") "-d" (str "resources/" id "/domain-" id ".idc")] (if events ["-q" query])))
            t-output (apply sh ["python3" (str ARCH "/instaltrace.py") "-j" (str "resources/" id "/json/") "-x" (str "resources/" id "/traces")])
            tracedir (clojure.java.io/file (str "resources/" id "/traces"))
            traces (filter #(.isFile %) (file-seq tracedir))
            sets (for [t traces]
                   (answer-set-to-map (slurp t)))]
        (do
          (spit debug output)
          (spit (str "resources/" id "/sets-" id ".edn") (prn-str sets))
          (spit outfile (:out output))
          (if (:out output)
            {:sets sets
             :text (:out output)}
            {:text output}))))))

(defn trope-map [trope]
  (let [parsed (make-map (parse-trope trope))]
    {:label (:label (:trope parsed))
     :events (:events (:trope parsed))
     :situations []})
  ;; also need: chars, obj, places?
  )

(defn st-map [name tropes chars objs places player]
  (let [trps (map trope-map tropes)
        role-pairs (map #(hash-map :class (:role %) :iname (:label %)) chars)
        obj-pairs (map #(hash-map :class (:type %) :iname (:label %)) objs)
        place-pairs (map #(hash-map :class (:location %) :iname (:label %)) places)
        story {:storyname name
               :tropes (map :label trps)
               :instances (concat role-pairs obj-pairs place-pairs)}
        ]
    {:story story
     :tropes trps
     :characters chars
     :objects objs
     :places places
     :player player
     }))

(defn make-cmd [t-files c-file o-file p-file oname player]
  (let [strs (map slurp t-files)
        c-strs (clojure.string/split-lines (slurp c-file))
        o-strs (clojure.string/split-lines (slurp o-file))
        p-strs (clojure.string/split-lines (slurp p-file))
        chars (map #(make-inst-map (parse-char %)) c-strs)
        objs (map #(make-inst-map (parse-object %)) o-strs)
        places (map #(make-inst-map (parse-place %)) p-strs)
        story-map (st-map oname strs chars objs places player)]
    (do
      (println "STORY:")
      (println story-map)
      (make-story story-map oname)
      (println "SUCCESS!")
      (println (str "Instal files are in the \"resources/" oname "\" directory.")))
    ))

