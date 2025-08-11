
openapi: 3.0.3
info:
  title: AIzahraAI - Qur'an & Multimedia API
  description: |
    API untuk proyek AIzahraAI - menyediakan akses data Al-Qur'an (arab, translit, terjemah),
    tajwid, audio per ayat, pencarian berbasis embedding/NLP, jadwal sholat & Hijri,
    text-to-speech (narasi) dan text→video endpoint.
  version: "0.1.0"
servers:
  - url: https://api.local.aizahra.ai/v1
    description: Local/Dev
tags:
  - name: quran
    description: Data Al-Qur'an (surah, ayat, tajwid)
  - name: audio
    description: Audio / streaming / per-ayat audio
  - name: tajwid
    description: Data dan markup tajwid
  - name: search
    description: Semantic search / embeddings
  - name: prayer
    description: Hijri & Prayer times (Aladhan / external)
  - name: tts
    description: Text-to-speech / narration
  - name: video
    description: Text→video generation & livestream helpers
security:
  - ApiKeyAuth: []
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
    OpenAIKey:
      type: apiKey
      in: header
      name: X-OpenAI-Key
    GoogleKey:
      type: apiKey
      in: header
      name: X-Google-Api-Key
  schemas:
    SurahSummary:
      type: object
      properties:
        number:
          type: integer
          example: 1
        name:
          type: string
          example: "Al-Fatihah"
        name_ar:
          type: string
          example: "الفاتحة"
        english_name:
          type: string
          example: "The Opening"
        verses_count:
          type: integer
          example: 7
    Verse:
      type: object
      properties:
        surah:
          type: integer
          example: 1
        ayat:
          type: integer
          example: 1
        arab:
          type: string
        arab_tajwid:
          type: string
        latin:
          type: string
        translation_id:
          type: string
    PrayerTimes:
      type: object
      properties:
        fajr: { type: string }
        sunrise: { type: string }
        dhuhr: { type: string }
        asr: { type: string }
        maghrib: { type: string }
        isha: { type: string }
        timezone: { type: string }
    HijriDate:
      type: object
      properties:
        date:
          type: string
          example: "13-02-1447"
        day_name:
          type: string
          example: "Al-Sabt"
    TTSRequest:
      type: object
      properties:
        text:
          type: string
        lang:
          type: string
          example: "id"
        voice:
          type: string
          example: "default"
    VideoRequest:
      type: object
      properties:
        text:
          type: string
        background_image_url:
          type: string
        duration:
          type: integer
          example: 30
        output_format:
          type: string
          enum: [mp4, rtmp]
paths:

  /surahs:
    get:
      tags: [quran]
      summary: List semua surah (ringkasan)
      responses:
        "200":
          description: Daftar surat
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/SurahSummary'

  /surahs/{surahId}:
    get:
      tags: [quran]
      summary: Detail sebuah surah (metadata + ayat ringkas)
      parameters:
        - name: surahId
          in: path
          required: true
          schema:
            type: integer
      responses:
        "200":
          description: Surah detail
          content:
            application/json:
              schema:
                type: object
                properties:
                  surah:
                    $ref: '#/components/schemas/SurahSummary'
                  verses:
                    type: array
                    items:
                      $ref: '#/components/schemas/Verse'

  /verses/{surahId}/{ayatId}:
    get:
      tags: [quran]
      summary: Ambil satu ayat lengkap (arab, tajwid, latin, terjemahan)
      parameters:
        - name: surahId
          in: path
          required: true
          schema: { type: integer }
        - name: ayatId
          in: path
          required: true
          schema: { type: integer }
      responses:
        "200":
          description: Ayat
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Verse'

  /audio/{surahId}/{ayatId}:
    get:
      tags: [audio]
      summary: URL audio per ayat (fallback ke audio full jika tidak ada per-ayat)
      parameters:
        - name: surahId
          in: path
          required: true
          schema: { type: integer }
        - name: ayatId
          in: path
          required: true
          schema: { type: integer }
      responses:
        "302":
          description: Redirect ke audio MP3 (pasang cache / CDN)
        "200":
          description: JSON berisi audio_url
          content:
            application/json:
              schema:
                type: object
                properties:
                  audio_url:
                    type: string
                    format: uri

  /tajwid/{surahId}/{ayatId}:
    get:
      tags: [tajwid]
      summary: Ambil markup tajwid (HTML/annotated text) untuk ayat
      parameters:
        - name: surahId
          in: path
          required: true
          schema: { type: integer }
        - name: ayatId
          in: path
          required: true
          schema: { type: integer }
      responses:
        "200":
          description: Tajwid markup (HTML fragment atau teks berwarna)
          content:
            application/json:
              schema:
                type: object
                properties:
                  arab_tajwid:
                    type: string
                  notes:
                    type: string

  /search:
    post:
      tags: [search]
      summary: Pencarian semantic (embedding) + fallback keyword
      description: |
        Menggunakan embedding (OpenAI atau model lokal) untuk menemukan ayat/ayat relevan, atau fallback ke pencocokan kata.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                q:
                  type: string
                top_k:
                  type: integer
                  default: 5
      responses:
        "200":
          description: Hasil pencarian
          content:
            application/json:
              schema:
                type: object
                properties:
                  query: { type: string }
                  results:
                    type: array
                    items:
                      type: object
                      properties:
                        surah: { type: integer }
                        ayat: { type: integer }
                        score: { type: number }
                        excerpt: { type: string }

  /prayer-times:
    get:
      tags: [prayer]
      summary: Jadwal sholat untuk koordinat (pakai Aladhan / lokal)
      parameters:
        - name: lat
          in: query
          required: true
          schema: { type: number, format: float }
        - name: lon
          in: query
          required: true
          schema: { type: number, format: float }
        - name: method
          in: query
          required: false
          schema: { type: integer }
      responses:
        "200":
          description: Jadwal sholat
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PrayerTimes'
                  - type: object
                    properties:
                      raw:
                        type: object
                        description: Response mentah dari provider

  /hijri:
    get:
      tags: [prayer]
      summary: Konversi tanggal Masehi → Hijri (atau ambil hari hijri sekarang)
      parameters:
        - name: date
          in: query
          required: false
          schema:
            type: string
            example: "2025-08-07"
        - name: tz
          in: query
          required: false
          schema:
            type: string
            example: "Asia/Jakarta"
      responses:
        "200":
          description: Tanggal Hijri
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HijriDate'

  /tts/narrate:
    post:
      tags: [tts]
      summary: Generate TTS dari teks narasi (menggunakan gTTS atau OpenAI TTS)
      security:

        - OpenAIKey: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TTSRequest'
      responses:
        "200":
          description: File audio TTS (URL)
          content:
            application/json:
              schema:
                type: object
                properties:
                  audio_url: { type: string, format: uri }
                  duration: { type: number }

  /video/generate:
    post:
      tags: [video]
      summary: Generate video MP4 dari teks (server-side render menggunakan FFmpeg / ImageMagick)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/VideoRequest'
      responses:
        "202":
          description: Accepted - rendering started (asynchronous)          content:
            application/json:
              schema:
                type: object
                properties:
                  job_id: { type: string }
                  status: { type: string, enum: [queued, processing] }
        "200":
          description: Direct MP4 (small)
          content:
            video/mp4:
              schema:
                type: string
                format: binary

  /video/stream:
    post:
      tags: [video]
      summary: Prepare RTMP stream target + overlay params (return rtmp url/key)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                title: { type: string }
                rtmp_destination: { type: string, example: "rtmp://a.rtmp.youtube.com/live2" }
                overlay_image_url: { type: string }
                show_map: { type: boolean, default: false }
      responses:
        "200":
          description: RTMP credentials / instructions
          content:
            application/json:
              schema:
                type: object
                properties:
                  rtmp_url: { type: string }
                  stream_key: { type: string }

  /utils/location:
    get:
      tags: [prayer]
      summary: Bantu konversi lat/lon → nama kota (reverse geocode). Gunakan Nominatim / Google Places.
      parameters:
        - name: lat
          in: query
          required: true
          schema: { type: number }
        - name: lon
          in: query
          required: true
          schema: { type: number }
      responses:
        "200":
          description: Nama tempat / kota
          content:
            application/json:
              schema:
                type: object
                properties:
                  city: { type: string }
                  region: { type: string }
                  country: { type: string }

  /admin/keys:
    get:
      tags: []
      summary: (Internal) List keys available to runtime (for UI only - do not expose publicly)
      security:
        - ApiKeyAuth: []l
      responses:
        "200":
          description: simple status
          content:
            application/json:
              schema:
                type: object
                properties:
                  openai: { type: boolean }
                  google: { type: boolean }
                  pixabay: { type: boolean }

components:
  # already declared above

externalDocs:
  description: Implementation notes - next steps
  url: https://your-docs-url.example.com


