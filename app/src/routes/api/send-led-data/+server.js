import dgram from 'dgram';

export async function POST({ request }) {
    const { ip, port, data } = await request.json();

    return new Promise((resolve, reject) => {
        const udpSocket = dgram.createSocket('udp4');
        const message = Buffer.from(data);

        udpSocket.send(message, port, ip, (err) => {
            udpSocket.close();
            if (err) {
                console.error('Error sending UDP packet:', err);
                reject(new Response('Failed to send LED data', { status: 500 }));
            } else {
                console.log('LED data sent successfully');
                resolve(new Response('LED data sent', { status: 200 }));
            }
        });
    });
}
