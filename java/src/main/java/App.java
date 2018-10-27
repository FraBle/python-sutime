import edu.stanford.nlp.python.SUTimeWrapper;

public class App {
    public static void main(String[] args) {
        SUTimeWrapper wrapper = new SUTimeWrapper(false, false, "spanish");
        System.out.println(wrapper.annotate("Hoy he escrito una prueba."));
    }
}
