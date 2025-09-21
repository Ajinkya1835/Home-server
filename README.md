# 🖥️ Home Server with Nextcloud, Cloudflare & Ubuntu

This repository documents how I transformed an **old laptop** into a **self-hosted cloud server**.  
Instead of paying for extra Google Drive storage, I built my own solution using **Ubuntu Server**, **Nextcloud**, and **Cloudflare** with a custom domain.  

---

## 🚀 Features
- 📂 **Nextcloud** for personal cloud storage  
- 🌐 Custom domain + **Cloudflare** for security and DNS  
- 🔑 Free **SSL/TLS certificates** (HTTPS)  
- ♻️ Reuse of old hardware (sustainable & cost-effective)  
- 🛠️ Hands-on learning with Linux, DNS, and server management  

---

## ⚙️ Setup Guide

### 1. Install Ubuntu Server
- Download the latest [Ubuntu Server ISO](https://ubuntu.com/download/server).  
- Create a bootable USB with [Rufus](https://rufus.ie/) (Windows) or `dd` (Linux/Mac).  
- Install Ubuntu Server on the old laptop.  
- Update system:  
  ```bash
  sudo apt update && sudo apt upgrade -y
