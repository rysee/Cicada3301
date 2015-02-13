class AES {
    public static void main(String[] args) {
        
        byte mult = (byte) 0x57; 
        byte mcand = (byte) 0x83;
        byte answer = multiplication(mult, mcand);
        System.out.println(Integer.toHexString((byte) answer));
        System.out.println(answer);
    }


    public static byte multiplication(byte multiplicand, byte multiplier) {
    	  // multiplicand == a, multiplier == b
        int product = 0;
        int test = 0;
        
        for (int i = 0; i < 8; i++) {
            
            test = multiplier & (byte) 1; // Gets rightmost bit of b
            
            
            if (test == 1) { // Tests to see if rightmost bit of a is set
                // If bit is set, XOR product with a
                product = product ^ multiplicand; 
            }
            
            multiplier = (byte) (multiplier >> 1); // Shift b 1 bit to the right. 
            // The above does not zero the multiplier's high bit. Will do below
            multiplier = (byte) (multiplier & (byte) 127);
            // 127 == 0111 1111  This should make highest bit 0
            // Basically a divide by two and drop the remainder
            // Check leftmost bit of a and call it the carry
            // Just AND by 1000 0000 == (byte) 128
            int carry = multiplicand & (byte) 128;
            if (carry == (byte) 128 ) {
                // Means leftmost bit of a is set
                // save one in carry
                carry = 1;
            } else {
                // Leftmost bit is 0
                carry = 0;
            }
            // Shift the multiplicand to the left one
            multiplicand = (byte) (multiplicand << 1);
            // If the carry was a one, XOR the multiplicand
            // with the irreducible polynomial mod 2.
            // The polynomial mod 2 is 00010010
            if (carry == 1) {
                multiplicand = (byte) (multiplicand ^ 0x1b);
            }
        }
    	  return (byte) product;
    }
}