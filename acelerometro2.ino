#include <inttypes.h>

static uint16_t ticks = 0;
static uint8_t counter = 0;

static uint16_t a[3] = { 0 };
#if 0
static struct {
    uint32_t X:10;
    uint32_t Y:10;
    uint32_t Z:10;
//    uint8_t padding;
} __attribute__((packed)) a = {0};
#endif

ISR(TIMER2_OVF_vect) {
    TCNT2 = 6;
    TIFR2 = 0x00;

#define SHIFT 5
    static uint16_t X = 0;
    static uint16_t Y = 0;
    static uint16_t Z = 0;

    /* demora ~333us */
    X += analogRead(A0);
    Y += analogRead(A1);
    Z += analogRead(A2);

    if (counter == (1<<SHIFT)){
        counter = 0;
#if 0
        a.X = X >> SHIFT;
        a.Y = Y >> SHIFT;
        a.Z = Z >> SHIFT;
#elif 0
        a[0] = X >> SHIFT;
        a[1] = Y >> SHIFT;
        a[2] = Z >> SHIFT;
#else
        a[0] = X;
        a[1] = Y;
        a[2] = Z;
#endif
        X = 0;
        Y = 0;
        Z = 0;
        ticks++;
    }
    counter++;
};  

void setup()
{
    analogReference(EXTERNAL);
    Serial.begin(57600);

    /* estamos a 2kHz */
    cli();
    TCCR2B = 0x00;
    TCNT2  = 6;
    TIFR2  = 0x00;
    TIMSK2 = 0x01;
    TCCR2A = 0x00;
    TCCR2B = 0x03;
    sei();

#if 0
    Serial.print("sizeof(a) ");
    Serial.println(sizeof(a));
    Serial.println("Inicializando");
    delay(200);
    Serial.println("Pronto");
#else
    delay(100);
#endif
}

void loop()
{
    static int ticks0 = 0;

    if (ticks != ticks0) {
//        Serial.write((uint8_t *) a, sizeof(a));
        Serial.print(a[0]);
        Serial.print('\t');
        Serial.print(a[1]);
        Serial.print('\t');
        Serial.print(a[2]);
        Serial.print('\n');
        ticks0 = ticks;
    }
}

