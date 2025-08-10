import serial
import time
try:
    ser=serial.Serial('COM3',9600,timeout=1)
    print('COM3 portu başarıyla açıldı.')
    time.sleep(1) 
except serial.SerialException as port_hatası:
    print(f"Hata: Seri porta bağlanılamadı. Lütfen COM3 portunu kontrol ediniz. {port_hatası}")
    exit()
except PermissionError as perm_:
    print(f" Port erişimi engellendi. Lütfen kontrol ediniz. {perm_}") 
    exit()   

son_durum=-1
def buton_kontrol(ser,durum):
    global son_durum
    if durum !=son_durum:
      try:
        if durum==1:
            ser.write(b'1')
            print(f"Butona basıldığı için Led yandı.")
        elif durum==0:
            ser.write(b'0')
            print(f"Butona basılmadığı için led yanmıyor.") 
        son_durum=durum 
      except Exception as err_:
        print(f"Led kontrol hatası: {err_}")          
def buton_durumu(ser):
        try:
            veri=ser.readline().decode('utf-8').strip()
            if not veri:
                return None
            if veri.isdigit():
                print(f"Arduinodan gelen veri: {veri}")
                gelen_durum=int(veri)
                if gelen_durum!=son_durum:
                    print(f"Arduinodan gelen veri: {gelen_durum}")
                return gelen_durum
            return None 
        except UnicodeDecodeError:
            print(f"Bozuk veri alındı")
            return None 
        except Exception as er:
            print(f"Arduinodan veri okuma hatası: {er}")
            return None 
try:
    print("\nButon ile LED kontrol uygulaması başlatıldı.")
    while True:
        durum=buton_durumu(ser)
        if durum is not None:
            buton_kontrol(ser,durum)
        time.sleep(0.01)
        
    
except KeyboardInterrupt:
    print(f"\nProgram sonlandırılıyor")
except Exception as ex_:
    print(f"Beklenmeyen bir hata oluştu: {ex_}")
    exit()
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print(f"Seri port kapatıldı.")    

           

 
