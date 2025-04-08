from flask import Flask, render_template_string,request, render_template
from datetime import datetime, timedelta
import re


app = Flask(__name__)

# Daftar pembaca (bisa diperbarui sesuai kebutuhan)
peserta_awal = [
    "H. Chambali", "Hj. Sri Astutik", "Hj. Pinatun", "Hj. Dwi Nur Kholifah",
    "H. Hariyanto", "Hj. Nuryati", "Hj. Farida", "Hj. Umi Nadliroh",
    "Hj. Arifah", "Hj. Mudawamah", "Hj. Ambar Asih", "H. Hari Saryono",
    "Hj. Umi Chatbirotin", "Hj. Ari Hanani", "Hj. Zuliani", "Hj. Khusnul",
    "Hj. Hidayati", "Hj. Diana Isnaeni", "Hj. Endang", "H. Fatkhur R",
    "Hj. Rini", "H. Moh Isfandi", "Hj. Umi Nadhiroh", "Hj. Yuniarti",
    "H. Jaka Purwita", "H. Jaka Purwita", "Hj. Siti Umayah", "H. Muhtar",
    "Hj. Elfi Riyana", "H. Muhaimin"
]

# Daftar pembaca doa khotmil Qur'an
pembaca_doa = ["H. Fatkhur R", "H. Jaka Purwita", "H. Muhtar", "H. Muhaimin",
               "H. Chambali", "H. Hariyanto", "H. Hari Saryono"]

# Periode pertama dimulai pada Jumat, 14 Maret 2025
periode_awal = datetime(2025, 3, 14)

@app.route("/")
def index():
    # Hitung periode saat ini berdasarkan hari ini
    hari_ini = datetime.today()
    selisih_hari = (hari_ini - periode_awal).days
    periode_sekarang = 43 + (selisih_hari // 7)

    # Hitung jumlah pergeseran
    shift_count = periode_sekarang - 43

    # Geser daftar peserta
    peserta_shifted = peserta_awal[-shift_count:] + peserta_awal[:-shift_count]

    # Tentukan pembaca doa berdasarkan giliran
    doa_khotmil_index = (shift_count) % len(pembaca_doa)
    pembaca_doa_terpilih = pembaca_doa[doa_khotmil_index]

    # Template HTML untuk ditampilkan di browser
    html_template = f"""
    <html>
    <head>
        <title>One Week One JUZ</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .container {{ max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ccc; }}
            pre {{ white-space: pre-wrap; word-wrap: break-word; background: #f8f8f8; padding: 10px; }}
            button {{ padding: 10px 20px; font-size: 16px; background: green; color: white; border: none; cursor: pointer; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>One Week One JUZ PERIODE {periode_sekarang}</h2>
            <h3>KHATAMAN AL QUR'AN Alumni Haji th 2023</h3>

            <pre id="textToCopy">
One Week One JUZ *PERIODE {periode_sekarang}*

KHATAMAN AL QUR'AN _Alumni Haji th 2023_

Awali Hadiah Fatihah Untuk
1. Nabi Muhammad SAW
2. Para Masyayikh
3. Seluruh Jamaah Haji
_Semoga diberikan keistiqomahan untuk terus belajar, memahami dan mengamalkan Al Quran_

""" + "\n".join([f"🕌 Juz {i:02d}. {nama}" for i, nama in enumerate(peserta_shifted, start=1)]) + f"""

Do'a Khotmil Qur'an ... Bpk. *{pembaca_doa_terpilih}*
Semoga Bacaan Al-Qur'an ini yang menjadi sebab dimudahkan Segala Urusan Oleh Allah SWT. 
Amiin 3x 🤲 Yaa Mujiibassaailiin
            </pre>

            <button onclick="copyText()">📋 Copy ke Clipboard</button>
            <script>
                function copyText() {{
                    var text = document.getElementById("textToCopy").innerText;
                    navigator.clipboard.writeText(text).then(function() {{
                        alert("Teks berhasil disalin! Sekarang tempel di WhatsApp.");
                    }}, function(err) {{
                        alert("Gagal menyalin teks.");
                    }});
                }}
            </script>
            <br><br>
            <a href="/">🔄 Refresh</a>
        </div>
    </body>
    </html>
    """
    return html_template

def proses_khataman(teks):
    semua_juz = set(range(1, 31))  # Semua juz dari 1-30
    juz_sudah = set()

    # Cari semua baris yang berisi "Juz xx."
    for line in teks.split("\n"):
        match = re.search(r'Juz (\d+)\.', line)
        if match:
            juz_num = int(match.group(1))  # Ambil nomor juz
            
            # Jika ada tanda 🕋 di akhir, anggap juz sudah dibaca
            if "🕋" in line:
                juz_sudah.add(juz_num)

    # Hitung juz yang belum dibaca
    juz_belum = semua_juz - juz_sudah

    return {
        "sudah_dibaca": sorted(juz_sudah),
        "belum_dibaca": sorted(juz_belum),
        "jumlah_sudah": len(juz_sudah),
        "jumlah_belum": len(juz_belum)
    }

@app.route("/hitung", methods=["GET", "POST"])
def hitung():
    hasil = {}
    if request.method == "POST":
        teks = request.form.get("textarea_khataman", "")
        hasil = proses_khataman(teks)
    
    return render_template("hitung.html", hasil=hasil)

if __name__ == "__main__":
    app.run(debug=True)

