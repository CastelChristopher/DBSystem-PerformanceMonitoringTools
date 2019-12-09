package javaclient;

import java.util.Random;

public interface Utils {
    Random rnd = new Random();

    class Tuple<A, B> {
        private final A a;
        private final B b;

        public Tuple(A a, B b) {
            this.a = a;
            this.b = b;
        }
    }
}
