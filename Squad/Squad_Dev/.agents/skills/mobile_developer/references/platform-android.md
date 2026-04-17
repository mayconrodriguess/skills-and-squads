# Android Platform Guide

Specifics that matter when shipping to Google Play. Pragmatic reference for
the Squad.

---

## 1. Modern Android Stack (2024-2025)

- **UI**: Jetpack Compose (recommended for new); XML views for legacy
- **Architecture**: MVVM with Android Architecture Components
- **State**: `ViewModel` + `StateFlow`
- **Concurrency**: Kotlin Coroutines + Flow
- **DI**: Hilt (Google recommended) or Koin
- **Data**: Room (SQLite wrapper), DataStore (preferences)
- **Networking**: Retrofit + OkHttp + kotlinx-serialization, or Ktor Client
- **Navigation**: Navigation-Compose
- **Testing**: JUnit 5 + Kotest + Espresso / Compose UI testing

---

## 2. Target SDK & Min SDK

Google Play enforces target SDK requirements annually. As of 2024, new apps
must target SDK 34 (Android 14); updates must target at least 33.

| API Level | Android |
|---|---|
| 24 | 7.0 Nougat |
| 26 | 8.0 Oreo |
| 28 | 9.0 Pie |
| 30 | 11 |
| 33 | 13 |
| 34 | 14 |
| 35 | 15 |

**Typical minimum**: SDK 24 (covers ~97% of active devices as of 2025). Lower
minimums let you reach older hardware but increase compat cost.

---

## 3. Permissions Model

### Install-time vs Runtime

- Install-time: declared in manifest, granted automatically (e.g., INTERNET)
- Runtime: request at use-time (CAMERA, LOCATION, MICROPHONE, READ_MEDIA_IMAGES)

### Manifest Declaration

```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
```

### Request at Use-Time (Compose)

```kotlin
val cameraPermission = rememberLauncherForActivityResult(
  ActivityResultContracts.RequestPermission()
) { isGranted ->
  // handle grant/deny
}

Button(onClick = { cameraPermission.launch(Manifest.permission.CAMERA) }) {
  Text("Use camera")
}
```

### Android 13+ Notifications

`POST_NOTIFICATIONS` became runtime in 13. Request it before sending any notification.

### Background Location / Background Activity

Google Play reviews apps requesting background location heavily. Provide a
clear justification and in-app explanation or expect rejection.

---

## 4. Data Safety (Play Console)

Required form; declares:
- Data types collected (personal info, device info, financial, etc.)
- Purpose (analytics, personalization, advertising)
- Shared with third parties?
- Encrypted in transit?
- Users can request deletion?

**Rule**: match your privacy policy exactly. Mismatch = enforcement action.

---

## 5. App Signing

- **Upload key**: used to sign APK/AAB you upload
- **App signing key**: managed by Play App Signing; signs the artifact delivered to devices

Keep the upload key private. If lost, Google can reset on request (if you have
the app signing key enrolled).

Use `.jks` or the Android keystore format; never commit to git.

---

## 6. Release Tracks

| Track | Purpose |
|---|---|
| Internal testing | Up to 100 testers, fast, no review |
| Closed testing | Email list or Google Groups, can have multiple |
| Open testing | Public link, listed (optional) on Play |
| Production | Staged rollout 1% → 5% → 20% → 50% → 100% |

Always use staged rollout in production. Watch ANR + crash rate before advancing.

---

## 7. App Bundle (AAB) Required

Since August 2021, Google Play requires `.aab` for new apps. Benefits:
- Smaller downloads per user (Play delivers only needed resources)
- Dynamic feature modules for on-demand features

Build: `./gradlew bundleRelease` (produces `.aab` in `app/build/outputs/bundle/release/`).

---

## 8. Proguard / R8 Obfuscation

Enable for release:

```kotlin
android {
  buildTypes {
    release {
      isMinifyEnabled = true
      proguardFiles(
        getDefaultProguardFile("proguard-android-optimize.txt"),
        "proguard-rules.pro"
      )
    }
  }
}
```

Add rules for reflection-based libraries (Gson, Moshi, Room entities, Retrofit service interfaces).

---

## 9. Push Notifications (FCM)

- Create Firebase project, add `google-services.json` to `app/`
- Subscribe `FirebaseMessagingService` for push
- Topic messaging OR device tokens
- Android 13+: request `POST_NOTIFICATIONS` before relying on notifications
- Notification channels (Android 8+): create channels for different importance levels

```kotlin
class MyFirebaseMessagingService : FirebaseMessagingService() {
  override fun onMessageReceived(msg: RemoteMessage) {
    // handle data payload and show a notification
  }
}
```

---

## 10. Deep Links & App Links

- Deep links: `<intent-filter>` with `android:scheme="myapp"` -- works but shows chooser
- **App Links**: verified `https://` URLs that open your app automatically

```xml
<intent-filter android:autoVerify="true">
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data android:scheme="https" android:host="yourdomain.com" />
</intent-filter>
```

Publish `assetlinks.json` at `https://yourdomain.com/.well-known/assetlinks.json`
with your app's SHA-256 signature.

---

## 11. Background Work

| API | Use |
|---|---|
| `WorkManager` | Deferrable, guaranteed work (uploads, sync) |
| `ForegroundService` | Ongoing user-visible tasks (music, navigation) -- requires notification |
| `AlarmManager` | Exact-time scheduling (reminders) |
| `JobScheduler` | System-optimized deferred jobs |

Android 14 tightened Foreground Service types -- declare `foregroundServiceType`
in manifest, match to the actual use case.

---

## 12. Security

### EncryptedSharedPreferences for secrets

```kotlin
val masterKey = MasterKey.Builder(context)
  .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
  .build()

val prefs = EncryptedSharedPreferences.create(
  context,
  "secure_prefs",
  masterKey,
  EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
  EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)
```

### Biometric gate

Use `androidx.biometric:biometric` — `BiometricPrompt` handles fingerprint, face,
strong authentication.

### Network Security Config

```xml
<network-security-config>
  <base-config cleartextTrafficPermitted="false">
    <trust-anchors>
      <certificates src="system" />
    </trust-anchors>
  </base-config>
</network-security-config>
```

### Root Detection

For financial / compliance apps, integrate Play Integrity API. Free, recommended
by Google to replace SafetyNet.

---

## 13. Performance Targets

- Cold start < 2s to visible content (baseline profiles help)
- < 30% dropped frames on scroll
- No ANRs (app not responding) — keep main thread < 100ms per frame
- App size < 50MB install; use dynamic delivery for larger assets

Tools:
- Android Studio Profiler (CPU, memory, energy, network)
- Baseline Profiles for startup speedup
- Macrobenchmark for realistic measurement
- R8 for shrinking release builds

---

## 14. Accessibility

- `contentDescription` on every icon / image
- Support TalkBack
- Ensure touch targets >= 48dp x 48dp
- Color contrast 4.5:1 for text
- Support large text: use `sp` units, respect system font scaling
- Test with Accessibility Scanner app from Google

---

## 15. Rejection / Policy Prevention

Before submitting:
- [ ] Target SDK matches current requirement
- [ ] All permissions have clear in-app justification
- [ ] Data Safety form matches privacy policy
- [ ] No use of sensitive permissions without necessity
- [ ] Foreground service types declared correctly
- [ ] Privacy policy + Terms accessible in-app
- [ ] No placeholder content
- [ ] Handles large screens / tablets / foldables if declared
- [ ] 64-bit support (mandatory since 2019)
- [ ] No crashes on rotation / dark mode
- [ ] Uninstall cleanly (no leftover services running)
