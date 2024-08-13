from scapy.all import ARP, Ether, srp

def ag_tarama(ip_araligi):
    """
    Verilen IP aralığındaki cihazları tarar ve IP ve MAC adreslerini döndürür.

    :param ip_araligi: Tarama yapılacak IP aralığı, örn: '192.168.1.1/24'
    :return: Cihazların IP ve MAC adreslerini içeren liste
    """
    # ARP isteği oluştur
    arp_request = ARP(pdst=ip_araligi)
    
    # Ethernet çerçevesi oluştur
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    
    # ARP isteğini Ethernet çerçevesine sar
    arp_request_broadcast = broadcast / arp_request
    
    # İsteği gönder ve yanıtları al
    yanitlar, _ = srp(arp_request_broadcast, timeout=2, verbose=False)
    
    cihazlar = []
    for yanit in yanitlar:
        cihaz = {'ip': yanit[1].psrc, 'mac': yanit[1].hwsrc}
        cihazlar.append(cihaz)
    
    return cihazlar
