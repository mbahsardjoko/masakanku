#!/usr/bin/env python3
import json

# Recipe content database
RECIPE_CONTENT = {
    'resep-sayur-asem-jakarta': {
        'intro': '''<p>Sayur asem Jakarta adalah comfort food sejati. Kuah asam segar, iga sapi empuk, sayuran lengkap — semua bersatu dalam satu mangkuk hangat.</p>
            <p>Berbeda dari sayur asem Sunda yang lebih encer, sayur asem Jakarta punya kuah lebih kental dengan rasa asam yang pas. Nggak terlalu tajam, tapi cukup segar buat bikin makan nasi makin lahap.</p>
            <p>Yang bikin spesial: kombinasi iga sapi dengan sayuran. Iga yang empuk dipadu dengan kacang panjang, jagung manis, labu siam, dan kacang tanah. Komplit.</p>
            <p>Dan resep ini nggak ribet. Kalau punya pressure cooker, iga bisa empuk dalam 30 menit. Kalau masak biasa, ya butuh 1.5 jam. Tapi hasilnya? Worth it banget.</p>''',
        'apa_itu': '''<p>Sayur asem Jakarta adalah sup sayur asam khas Betawi. Berbeda dari sayur asem Sunda yang vegetarian, versi Jakarta selalu pakai iga sapi atau daging sapi.</p>
            <p>Kuahnya dibuat dari asam jawa yang dilarutkan, ditambah bumbu aromatik seperti bawang merah, bawang putih, lengkuas, dan daun salam. Hasilnya kuah berwarna kecokelatan dengan rasa asam yang khas.</p>
            <p>Sayuran yang dipakai: kacang panjang, jagung manis, labu siam, kacang tanah mentah. Kadang ada yang nambah melinjo atau nangka muda. Tergantung selera keluarga masing-masing.</p>''',
        'bahan': '''<h3>Bahan Utama:</h3>
            <ul>
                <li>500 gram iga sapi (potong per ruas)</li>
                <li>2 liter air</li>
                <li>1 tongkol jagung manis (potong 4 bagian)</li>
                <li>200 gram kacang panjang (potong 5 cm)</li>
                <li>200 gram labu siam (potong dadu)</li>
                <li>100 gram kacang tanah mentah</li>
                <li>3 buah tomat merah (potong wedges)</li>
                <li>2 buah asam jawa ukuran telur puyuh (larutkan dengan 100ml air)</li>
            </ul>
            <h3>Bumbu Halus:</h3>
            <ul>
                <li>6 siung bawang merah</li>
                <li>4 siung bawang putih</li>
                <li>2 cm lengkuas</li>
                <li>1 sdt terasi bakar</li>
            </ul>
            <h3>Bumbu Pelengkap:</h3>
            <ul>
                <li>3 lembar daun salam</li>
                <li>2 batang serai (geprek)</li>
                <li>2 cm lengkuas (geprek)</li>
                <li>1 sdm garam</li>
                <li>1 sdt gula merah</li>
                <li>1/2 sdt merica bubuk</li>
            </ul>''',
        'cara': '''<h3>Langkah 1: Rebus Iga</h3>
            <ol>
                <li>Rebus iga sapi dengan 2 liter air. Buang busa yang muncul di permukaan.</li>
                <li>Masak dengan api sedang selama 1.5 jam sampai iga empuk. Kalau pakai pressure cooker, cukup 30 menit.</li>
                <li>Angkat iga, sisihkan. Saring kaldu, buang ampas.</li>
            </ol>
            <h3>Langkah 2: Tumis Bumbu</h3>
            <ol>
                <li>Haluskan bumbu halus: bawang merah, bawang putih, lengkuas, dan terasi.</li>
                <li>Panaskan 2 sdm minyak. Tumis bumbu halus sampai harum dan matang.</li>
                <li>Masukkan daun salam, serai, dan lengkuas geprek. Aduk rata.</li>
            </ol>
            <h3>Langkah 3: Masak Sayur Asem</h3>
            <ol>
                <li>Tuang kaldu iga ke dalam wajan bumbu. Didihkan.</li>
                <li>Masukkan iga sapi yang sudah direbus. Masak 10 menit.</li>
                <li>Tambahkan kacang tanah dan jagung. Masak 15 menit sampai kacang empuk.</li>
                <li>Masukkan labu siam. Masak 5 menit.</li>
                <li>Terakhir, masukkan kacang panjang dan tomat. Masak 3 menit.</li>
                <li>Tuang air asam jawa. Aduk rata.</li>
                <li>Bumbui dengan garam, gula merah, dan merica. Koreksi rasa.</li>
                <li>Matikan api. Sajikan panas dengan nasi putih dan sambal.</li>
            </ol>''',
        'rahasia': '''<p><strong>Iga Harus Empuk Dulu</strong></p>
            <p>Jangan langsung masak semua bahan bareng. Rebus iga dulu sampai empuk. Kaldu dari iga ini yang jadi base flavor sayur asem. Kalau iga masih keras, sayur asem nggak akan sempurna.</p>
            <p><strong>Asam Jawa Masuk Terakhir</strong></p>
            <p>Jangan masukkan air asam dari awal. Tunggu semua sayuran matang baru tuang. Kalau terlalu cepat, sayuran bisa jadi alot dan warnanya kusam.</p>
            <p><strong>Gula Merah Bikin Kuah Lebih Nikmat</strong></p>
            <p>Gula merah nggak cuma pemanis. Dia bikin rasa kuah lebih kompleks dan balance. Asam, manis, gurih — semua harmonis.</p>''',
        'variasi': '''<h3>Sayur Asem Iga Presto</h3>
            <p>Pakai iga presto yang sudah jadi. Tinggal masak bumbu dan sayuran, masukkan iga presto di akhir. Lebih cepat dan praktis.</p>
            <h3>Sayur Asem Daging Giling</h3>
            <p>Ganti iga dengan daging sapi giling yang dibentuk bola-bola kecil. Lebih ekonomis dan anak-anak suka.</p>
            <h3>Sayur Asem Vegetarian</h3>
            <p>Hilangkan iga, pakai kaldu jamur atau kaldu sayur. Tambahkan tahu dan tempe biar protein tetap cukup.</p>''',
        'tips_icon': '🥗',
        'tips': '''<li><strong>Pilih iga yang berlemak.</strong> Lemak di sekitar tulang bikin kaldu lebih gurih dan kuah lebih nikmat.</li>
                <li><strong>Jangan overcook sayuran.</strong> Kacang panjang cukup 3 menit. Labu siam 5 menit. Biar tetap renyah dan warnanya cantik.</li>
                <li><strong>Air asam jawa harus disaring.</strong> Serat asam bisa bikin tekstur kuah kasar. Saring pakai saringan kawat halus.</li>
                <li><strong>Koreksi rasa di akhir.</strong> Setiap asam jawa punya tingkat keasaman beda. Cicipi dan sesuaikan dengan tambahan gula atau garam.</li>
                <li><strong>Lebih enak dimakan besok.</strong> Sayur asem makin sedap setelah bumbu meresap. Hangatkan kembali sebelum disajikan.</li>''',
        'kenapa': '''<p>Sayur asem Jakarta adalah bukti bahwa comfort food nggak harus mahal atau ribet. Bahan-bahannya sederhana, prosesnya straightforward, tapi hasilnya? Bikin kangen rumah.</p>
            <p>Ini hidangan yang cocok buat segala cuaca. Pas hujan, kuah hangatnya bikin nyaman. Pas panas, rasa asamnya segar dan bikin makan jadi lahap.</p>
            <p>Dan yang paling penting: satu panci sayur asem bisa buat makan sekeluarga. Hemat, praktis, dan pasti habis. Cocok banget buat makan malam atau bekal esok hari.</p>''',
        'faq': '''<p><strong>Sayur asem tahan berapa lama?</strong></p>
            <p>Di kulkas tahan 3 hari. Panaskan kembali sebelum makan. Jangan dihangatkan berkali-kali, sayuran bisa jadi lembek.</p>
            <p><strong>Bisa pakai daging tanpa tulang?</strong></p>
            <p>Bisa. Pakai daging has dalam atau sandung lamur. Potong dadu, rebus sampai empuk. Tapi kaldu dari iga lebih gurih.</p>
            <p><strong>Asam jawa bisa diganti apa?</strong></p>
            <p>Belimbing wuluh atau tomat hijau yang lebih banyak. Tapi rasa khas sayur asem ya dari asam jawa.</p>
            <p><strong>Kenapa sayuran jadi lembek?</strong></p>
            <p>Overcooked. Masukkan sayuran bertahap: kacang tanah dan jagung dulu, labu siam, baru kacang panjang terakhir. Masing-masing punya waktu masak berbeda.</p>
            <p><strong>Bisa dibekukan?</strong></p>
            <p>Bisa, tapi sayuran akan berubah tekstur setelah dicairkan. Lebih baik bekukan iga dan kaldunya aja, masak sayuran fresh waktu mau makan.</p>''',
        'cta': '''<p>Yuk bikin sayur asem Jakarta yang bikin makan nasi makin lahap!</p>
            <p>Siapkan iga, sayuran, dan asam jawa. 2 jam lagi, kamu punya panci penuh comfort food yang bikin keluarga happy. Selamat masak! 🥗</p>''',
        'baca_juga': [
            ('soto-ayam', 'Resep Soto Ayam Kuning Gurih'),
            ('resep-sayur-lodeh', 'Resep Sayur Lodeh Santan Gurih'),
            ('resep-rendang-daging', 'Resep Rendang Daging Empuk'),
            ('resep-gulai-ayam', 'Resep Gulai Ayam Khas Padang')
        ]
    }
}

print("Content database loaded")
print(f"Recipes: {list(RECIPE_CONTENT.keys())}")
