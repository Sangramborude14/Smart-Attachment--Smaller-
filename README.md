---

# ? Ad-Blocking DNS Server using Raspberry Pi Zero

## ? Overview

This project uses a **Raspberry Pi Zero** to create a **DNS server** that filters out ad-related domains and blocks them before they reach your device. It leverages **Pi-hole**, a powerful open-source software for network-wide ad blocking.

By routing your device?s DNS queries through the Pi Zero, all ad requests are intercepted and blocked, resulting in a faster and cleaner browsing experience.

---

## ?? Components

* ? **Raspberry Pi Zero (W or 2 recommended)**
* ? **Micro SD Card (8GB or higher)**
* ? **Power Supply (5V, 2A recommended)**
* ? **Wi-Fi or Ethernet Connection**
* ?? **Any client device (PC, phone, or tablet)**

---

## ? Working Principle

1. The **Pi-hole** software turns your **Raspberry Pi Zero** into a **local DNS server**.
2. All DNS queries from your devices go through the **Pi Zero** first.
3. Pi-hole filters the requests and blocks domains known for ads or trackers.
4. Clean data packets are then sent to your device, keeping browsing fast and ad-free.

---

## ? Setup Instructions

1. **Install Raspberry Pi OS** on the SD card using [Raspberry Pi Imager](https://www.raspberrypi.com/software/).
2. Boot up the Pi and connect it to the internet.
3. Open the terminal and run:

   ```bash
   curl -sSL https://install.pi-hole.net | bash
   ```
4. Follow the on-screen instructions to configure Pi-hole as your DNS server.
5. Set the Pi-hole?s IP address as the **DNS server** on your device or router.
6. Access the web dashboard at:

   ```
   http://<your-pi-ip-address>/admin
   ```

---

## ? Features

* Network-wide ad blocking
* Easy-to-use web dashboard
* Lightweight and runs efficiently on Raspberry Pi Zero
* Can be used with multiple devices simultaneously

---

## ? How It Works (Simplified)

```
Your Device ? Raspberry Pi Zero (Pi-hole) ? Internet
```

* The Pi Zero acts as a **middleman** between your device and the internet.
* It filters DNS requests and blocks ad domains before they load.

---

## ? Example Use Case

You connect your phone to the same Wi-Fi network as the Raspberry Pi Zero.
When you open a website, instead of loading ads, Pi-hole silently blocks them and only lets the useful content through.

---

## ? Future Improvements

* Add a custom blacklist/whitelist
* Integrate statistics on blocked domains
* Use Raspberry Pi Zero 2 for better performance

---

## ? References

* [Pi-hole Official Website](https://pi-hole.net/)
* [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)

---
