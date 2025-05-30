import java.math.BigInteger;
import java.util.Random;

public class RSA {

    
    public static BigInteger generatePrime(int bits) {
        Random rand = new Random();
        BigInteger prime;
        do {
            prime = new BigInteger(bits, rand);
        } while (!prime.isProbablePrime(100)); 
        return prime;
    }

    public static BigInteger gcd(BigInteger a, BigInteger b) {
        while (!b.equals(BigInteger.ZERO)) {
            BigInteger temp = a;
            a = b;
            b = temp.mod(b);
        }
        return a;
    }

    public static BigInteger modInverse(BigInteger e, BigInteger phi) {
        BigInteger[] result = extendedGcd(e, phi);
        BigInteger d = result[1];
        if (d.compareTo(BigInteger.ZERO) < 0) {
            d = d.add(phi); 
        }
        return d;
    }
    public static BigInteger[] extendedGcd(BigInteger a, BigInteger b) {
        BigInteger old_r = a, r = b;
        BigInteger old_s = BigInteger.ONE, s = BigInteger.ZERO;
        BigInteger old_t = BigInteger.ZERO, t = BigInteger.ONE;

        while (!r.equals(BigInteger.ZERO)) {
            BigInteger quotient = old_r.divide(r);
            BigInteger temp_r = r;
            r = old_r.subtract(quotient.multiply(r));
            old_r = temp_r;

            BigInteger temp_s = s;
            s = old_s.subtract(quotient.multiply(s));
            old_s = temp_s;

            BigInteger temp_t = t;
            t = old_t.subtract(quotient.multiply(t));
            old_t = temp_t;
        }
        return new BigInteger[] { old_r, old_s, old_t };
    }
    public static BigInteger[] generateRSAKeys(int bits) {
        BigInteger p = generatePrime(bits);
        BigInteger q = generatePrime(bits);
        BigInteger n = p.multiply(q);
        BigInteger phi = (p.subtract(BigInteger.ONE)).multiply(q.subtract(BigInteger.ONE));

        BigInteger e = BigInteger.valueOf(65537); // Common choice for public exponent
        if (gcd(e, phi).compareTo(BigInteger.ONE) != 0) {
            throw new IllegalArgumentException("e and phi(n) are not coprime");
        }

        BigInteger d = modInverse(e, phi);

        return new BigInteger[] { n, e, d };
    }

    public static BigInteger encrypt(BigInteger n, BigInteger e, BigInteger message) {
        return message.modPow(e, n);
    }

    public static BigInteger decrypt(BigInteger n, BigInteger d, BigInteger ciphertext) {
        return ciphertext.modPow(d, n);
    }

    public static void main(String[] args) {
        try {
            int bits = 17;  
            BigInteger[] keys = generateRSAKeys(bits);

            BigInteger n = keys[0];
            BigInteger e = keys[1];
            BigInteger d = keys[2];

        
            System.out.println("Public Key: (" + n + ", " + e + ")");
            
            System.out.println("Private Key: (" + n + ", " + d + ")");

           
            BigInteger message = BigInteger.valueOf(42);  
            BigInteger ciphertext = encrypt(n, e, message);
            System.out.println("Encrypted: " + ciphertext);

           
            BigInteger decryptedMessage = decrypt(n, d, ciphertext);
            System.out.println("Decrypted: " + decryptedMessage);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
