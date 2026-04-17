---
name: mobile-developer
description: >
  Build or refactor mobile applications (iOS, Android, cross-platform) from
  approved architecture artifacts.
  TRIGGERS: mobile, ios, android, react native, expo, flutter, dart, swift,
  swiftui, kotlin, jetpack compose, kmm, kotlin multiplatform, native,
  cross-platform, app store, play store, testflight, apns, fcm, push,
  deeplink, universal link, app clip, in-app purchase, storekit, keychain,
  keystore, biometrics, face id, touch id, fingerprint, sensor, camera,
  geolocation, offline, sync, sqlite, realm, watermelondb, drizzle mobile,
  app-store-connect, fastlane, eas, xcode, gradle, android studio.
---

# Mobile Developer

## Objective

Choose the right mobile approach for the project, implement it in `app_build/`,
and leave a clear release path for iOS and Android. Mobile is not web -- touch,
thumb zones, offline resilience, battery, and app-store policies are first-class
constraints.

**Core principle**: The best mobile stack is the one that matches the team,
the product requirements, and the delivery timeline -- in that order.

---

## 1. Project Structure Contract

| Folder | Purpose |
|---|---|
| `production_artifacts/Mobile_Architecture.md` | Approved mobile stack + rationale |
| `app_build/` | Mobile codebase |
| `app_build/src/` (RN/Flutter) or `ios/`, `android/` (native) | Source per platform |
| `app_build/e2e/` | Detox / Maestro flows |
| `scripts/mobile/` | Setup, build, release helpers |
| `assets/branding/` | App icons, splash, adaptive icons |
| `references/` | Platform notes, store review findings |
| `.agents/workflows/mobile-release.md` | Release cadence if repeated |

---

## 2. Required Inputs

| Document | Required | Why |
|---|---|---|
| `production_artifacts/Technical_Specification.md` | YES | Features, user flows |
| `production_artifacts/Solution_Architecture.md` | YES | Backend contracts, auth model |
| `production_artifacts/Tech_Stack_Rationale.md` | When present | Framework choice |
| `production_artifacts/API_Contract.md` | When present | Endpoints, payload shapes |

---

## 3. Framework Decision Tree

Never default to a favorite. Match to the project:

| Criteria | React Native (+Expo) | Flutter | Native (Swift + Kotlin) | KMM |
|---|---|---|---|---|
| Team already knows TS/JS | Best fit | Ramp up | Deep ramp | Partial |
| Team knows Dart | Not applicable | Best fit | Not applicable | Not applicable |
| Team is mostly iOS/Android devs | Could work | Could work | Best fit | Best fit |
| Heavy custom UI / animations | Good | Best (60fps Skia) | Best (full control) | Depends on UI layer |
| Deep device integration (AR, Bluetooth LE, sensors) | Good with native modules | Good with plugins | Best | Best |
| Shared logic between web + mobile | Best (RN + React web) | Limited | No | Partial |
| MVP in 6-8 weeks | Best | Best | Slowest | Between |
| Long-term single codebase | Good | Good | Most cost over time | Good if team fits |
| App Store / Play Store review risk | Usual rules | Usual rules | Lowest friction | Usual rules |

**Shortcut guidance**:
- Small team, web + mobile, tight deadline → **React Native + Expo**
- Design-heavy, pixel-perfect, single mobile target → **Flutter**
- Performance critical + platform-specific UX → **Native**
- Business logic shared, UI native → **KMM** (Kotlin Multiplatform Mobile)

Document the decision as an ADR.

---

## 4. Workflow

### Phase 1 -- Analyze
1. Read spec + architecture
2. Identify device capabilities needed (camera, location, push, biometrics)
3. Determine offline requirements and sync strategy
4. Confirm backend API contract

### Phase 2 -- Decide
5. Apply Framework Decision Tree, write ADR
6. Pick navigation, state management, data layer per the stack

### Phase 3 -- Scaffold
7. Create project (`npx create-expo-app`, `flutter create`, Xcode/Android Studio)
8. Set up CI build (EAS, Codemagic, Bitrise, GitHub Actions)
9. Configure lint, format, type-check, test
10. Set up env management per platform

### Phase 4 -- Implement
11. Build features by user flow, not by platform
12. Apply touch-first UX (see Section 6)
13. Handle states: loading / empty / error / offline / permission-denied
14. Integrate push notifications early (needs certs / keys)
15. Implement auth + secure storage (Keychain iOS / Keystore Android)

### Phase 5 -- Release Prep
16. App icons + splash screens + adaptive icons
17. Privacy manifest (iOS), data safety form (Play)
18. Permissions strings (Info.plist, AndroidManifest)
19. In-app purchase SKUs (if applicable)
20. Store screenshots and copy

### Phase 6 -- Ship
21. Internal test → TestFlight / Internal Testing track
22. External beta → closed testing
23. Staged rollout (1% → 10% → 50% → 100%)
24. Crash + analytics dashboards watched for 7 days

---

## 5. Cross-Platform Stack Details

See the deep-dives in:
- [references/platform-ios.md](references/platform-ios.md) — iOS-specific
- [references/platform-android.md](references/platform-android.md) — Android-specific
- [references/mobile-performance.md](references/mobile-performance.md) — perf + battery + memory

### React Native + Expo (recommended default for JS teams)

- **Navigation**: Expo Router (file-based) or React Navigation
- **State**: Zustand / TanStack Query
- **Data**: MMKV (fast KV), WatermelonDB or Drizzle for SQLite
- **Forms**: React Hook Form + Zod
- **Notifications**: `expo-notifications`
- **Secure storage**: `expo-secure-store`
- **Build / Release**: EAS Build + EAS Submit
- **OTA updates**: EAS Update (follow store rules: no breaking changes via OTA)

### Flutter

- **Navigation**: `go_router`
- **State**: Riverpod (prefer) or Bloc
- **Data**: Drift (SQLite), Isar, Hive
- **Forms**: `flutter_form_builder`
- **Notifications**: `firebase_messaging`
- **Secure storage**: `flutter_secure_storage`
- **Build / Release**: Codemagic or `flutter build` + Fastlane

### Native Swift (iOS)

- **UI**: SwiftUI for greenfield; UIKit for legacy interop
- **Concurrency**: async/await + actors
- **Data**: SwiftData (iOS 17+) or Core Data; GRDB for raw SQL
- **Networking**: URLSession + async
- **DI**: Swift Package with a composition root
- **Build**: Xcode Cloud or Fastlane

### Native Kotlin (Android)

- **UI**: Jetpack Compose
- **Concurrency**: Coroutines + Flow
- **Data**: Room (SQLite), DataStore
- **Networking**: Retrofit + OkHttp + kotlinx-serialization or Ktor Client
- **DI**: Hilt or Koin
- **Build**: Gradle + Fastlane or GitHub Actions

---

## 6. Touch-First UX

### Targets and Thumb Zones

- Minimum touch target: **44x44pt iOS**, **48x48dp Android**
- Primary CTAs in the **thumb-friendly zone** (bottom half of screen for one-handed use)
- Spacing between taps >= 8dp/pt to avoid accidental hits

### Fitts' Law Applied

- Bigger target + closer distance = faster interaction
- Tab bar (bottom) > hamburger menu for frequent actions
- Floating Action Button reserved for the single most important action

### Motion + Feedback

- Every touch has instant visual feedback (<100ms)
- Haptics for meaningful confirmations (avoid spam)
- Respect `prefers-reduced-motion` equivalents
- Animations <= 400ms, easing that matches platform (iOS: `easeInOut`; Android: standard curves)

### Platform Conventions

- iOS: back chevron top-left, share sheet, pull-to-refresh, swipe to delete
- Android: back gesture + system back, snackbar for confirmations, Material You theming

### States Every Screen Must Handle

- Loading (skeleton > spinner when possible)
- Empty (explain + action)
- Error (actionable message, retry)
- Offline (queue + sync later, or read-only)
- Permission denied (explain why + deep link to Settings)

---

## 7. Offline & Sync

Mobile users lose connectivity. Plan for it:

| Approach | Use When |
|---|---|
| Read-only cache | Content consumption apps |
| Write-through cache | Fast UI + immediate sync when online |
| Offline-first queue | Forms, draft data, fire-and-forget mutations |
| CRDT sync | Collaborative docs, complex merges |

Libraries: WatermelonDB, RxDB, PowerSync, Replicache, Automerge.

### Optimistic Updates

Always show the action as successful immediately; reconcile on server response.
Handle failure by rolling back + showing a toast.

---

## 8. Push Notifications

- iOS: APNs (configure .p8 key or .p12 cert in App Store Connect)
- Android: FCM (Firebase project + `google-services.json`)
- Token registration on login, de-registration on logout
- Deep-link payload: route + IDs, never sensitive data in the notification body
- Request permission at a meaningful moment, not at app launch

---

## 9. Security Essentials

- Store tokens in Keychain (iOS) / EncryptedSharedPreferences or Keystore (Android)
- No secrets in JS bundle / Dart bundle / source code
- Certificate pinning for critical endpoints (auth, payment)
- Jailbreak / root detection for financial / compliance apps
- OWASP MASVS Level 1 minimum; Level 2 for sensitive apps
- Privacy manifest (`PrivacyInfo.xcprivacy`) on iOS 17+
- Data Safety form on Play Console: declare all data collection truthfully

---

## 10. Release Checklist

### iOS (App Store)

- [ ] Bundle ID + Team + capabilities
- [ ] App icons (all sizes) + launch screen
- [ ] Privacy manifest
- [ ] Usage strings for every permission in Info.plist
- [ ] App Store screenshots (6.7", 5.5")
- [ ] Privacy policy URL
- [ ] Age rating
- [ ] IDFA declaration (if used)
- [ ] TestFlight tested with real users
- [ ] Version + build number incremented
- [ ] App Store Connect compliance answered

### Android (Play Store)

- [ ] Package name, signing key (upload key + app signing)
- [ ] Adaptive + legacy icons
- [ ] Feature graphic, screenshots per device type
- [ ] Data safety form
- [ ] Target SDK matches Play Store requirement (current: 34+)
- [ ] Privacy policy URL
- [ ] Content rating
- [ ] Internal testing → closed → production with staged rollout

---

## 11. Quality Bar

- [ ] Framework chosen per project constraints with ADR
- [ ] Secure storage used for tokens + sensitive data
- [ ] Navigation + state management justified
- [ ] All screens handle loading/empty/error/offline/permission states
- [ ] Push notifications end-to-end tested
- [ ] Release build tested on real device, not just simulator
- [ ] App icons + splash + store assets ready
- [ ] Crash reporter + analytics instrumented
- [ ] Store compliance forms completed
- [ ] CI builds signed release artifacts
- [ ] Rollback strategy documented

---

## 12. Bundled Reference

| File | Contents |
|---|---|
| [references/platform-ios.md](references/platform-ios.md) | iOS specifics: SwiftUI, App Clips, In-App Purchase, entitlements |
| [references/platform-android.md](references/platform-android.md) | Android specifics: Compose, Jetpack, target SDK, Play policies |
| [references/mobile-performance.md](references/mobile-performance.md) | Rendering, startup, battery, memory, bundle size |

---

## 13. Deliverables

Every mobile task produces:

1. `production_artifacts/Mobile_Architecture.md` with framework ADR
2. Mobile codebase in `app_build/`
3. Build + release scripts in `scripts/mobile/`
4. Store assets in `assets/branding/`
5. Release checklist filled per platform
6. Updated `production_artifacts/memory/AI_CONTEXT.md`
