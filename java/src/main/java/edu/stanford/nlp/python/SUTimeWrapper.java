package edu.stanford.nlp.python;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.*;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.time.SUTime;
import edu.stanford.nlp.time.TimeAnnotations;
import edu.stanford.nlp.time.TimeExpression;
import edu.stanford.nlp.util.CoreMap;
import edu.stanford.nlp.util.PropertiesUtils;

public class SUTimeWrapper {

    private Properties properties;
    private StanfordCoreNLP pipeline;
    private DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
    private Gson gson;

    public SUTimeWrapper(boolean markTimeRanges, boolean includeRange) {
        this.properties = PropertiesUtils.asProperties(
                "customAnnotatorClass.sutime", "edu.stanford.nlp.time.TimeAnnotator",
                "sutime.markTimeRanges", markTimeRanges ? "true" : "false",
                "sutime.includeRange", includeRange ? "true" : "false",
                "annotators", "tokenize, ssplit, pos, lemma, ner, sutime",
                "ner.useSUTime", "true"
        );
        this.pipeline = new StanfordCoreNLP(this.properties);
        this.gson = new Gson();
    }

    public String annotate(String input) {
        String today = this.dateFormat.format(Calendar.getInstance().getTime());
        Annotation annotation = new Annotation(input);
        annotation.set(CoreAnnotations.DocDateAnnotation.class, today);

        this.pipeline.annotate(annotation);
        List<CoreMap> timexAnnotations = annotation.get(TimeAnnotations.TimexAnnotations.class);

        List<Map> result = new ArrayList<Map>();


        for (CoreMap coreMap : timexAnnotations) {
            List<CoreLabel> tokens = coreMap.get(CoreAnnotations.TokensAnnotation.class);
            String type = coreMap.get(TimeAnnotations.TimexAnnotation.class).timexType();
            SUTime.Time durationBegin = coreMap.get(TimeExpression.Annotation.class).getTemporal().getRange().begin();
            SUTime.Time durationEnd = coreMap.get(TimeExpression.Annotation.class).getTemporal().getRange().end();

            HashMap<String, Object> resultEntry = new HashMap<>();
            resultEntry.put("text", coreMap.toString());
            resultEntry.put("start", tokens.get(0).get(CoreAnnotations.CharacterOffsetBeginAnnotation.class));
            resultEntry.put("end", tokens.get(tokens.size() - 1).get(CoreAnnotations.CharacterOffsetEndAnnotation.class));
            resultEntry.put("type", type);

            if (type.equals("DURATION") && durationBegin != null && durationEnd != null){
                HashMap<String, String> valueMap = new HashMap<>();
                valueMap.put("begin", durationBegin.toISOString());
                valueMap.put("end", durationEnd.toISOString());
                resultEntry.put("value", valueMap);
            } else{
                resultEntry.put("value", coreMap.get(TimeExpression.Annotation.class).getTemporal().toISOString());
            }

            result.add(resultEntry);
        }
        return this.gson.toJson(result, new TypeToken<List<Map>>() {}.getType());
    }
}

