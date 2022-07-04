import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;


public class sendImage{

    public static void main(String[] args) throws Exception {
        ServerSocket ss = new ServerSocket(6001);
        Socket socket = ss.accept();
       
        while(true){
            File image = new File("img.jpg");
            if(image != null){
                OutputStream outputStream = socket.getOutputStream();

                BufferedImage Bimage = ImageIO.read(image);
            
                ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
                ImageIO.write(Bimage, "jpg", byteArrayOutputStream);
            
                byte[] size = ByteBuffer.allocate(4).putInt(byteArrayOutputStream.size()).array();
                outputStream.write(size);
                outputStream.write(byteArrayOutputStream.toByteArray());
                System.out.println("Imagen enviada");
                outputStream.flush();
                Thread.sleep(2000);
            }
        }
    }
}
