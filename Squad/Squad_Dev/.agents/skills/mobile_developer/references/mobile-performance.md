# Mobile Performance Guide

Rendering, startup, battery, memory, bundle size. Mobile users punish slow
apps faster than web users -- they uninstall.

---

## 1. Startup Time

### Targets

- Cold start: < 2s to first meaningful content
- Warm start: < 1s
- Hot start: < 500ms

### Common Causes of Slow Startup

- Heavy work in `Application.onCreate()` / `AppDelegate.application(didFinishLaunching)`
- Synchronous network calls at launch
- Large asset decoding on main thread
- Initialization of libraries not needed on first screen

### Fixes

- Defer initializations until after first frame
- Splash screen that transitions seamlessly to first UI
- Baseline Profiles (Android) / Background Asset Downloader (iOS)
- Lazy-load modules (Hermes, Compose code splitting)
- Measure: Android Studio Startup, Xcode Instruments Time Profiler

---

## 2. Rendering / Jank

### Target

60fps (or 120fps on ProMotion iPhones + Android high-refresh) = **16.6ms per frame** (or **8.3ms**).

### Sources of Jank

- Main thread work (DB, network, image decode)
- Overdraw (multiple layers redrawing same pixels)
- Large lists without virtualization
- Complex animations on low-end devices
- Synchronous JS bridge calls (RN old architecture)

### Fixes

| Platform | Tool |
|---|---|
| iOS | Instruments → Core Animation |
| Android | Systrace, Perfetto |
| RN | Flipper, Hermes profiler |
| Flutter | DevTools Performance view |

- Move non-UI work off main thread
- Flatten view hierarchies
- `FlatList` / `RecyclerView` / `LazyColumn` for long lists
- Image caching (Coil, Kingfisher, FastImage)
- Compose: `derivedStateOf`, stable classes, avoid unnecessary recomposition

---

## 3. Memory

### Typical Budgets

- Background: < 50 MB
- Active: < 150 MB
- Peak: < 300 MB

Breach these and the OS kills your app on low-memory devices.

### Common Leaks

- Activity / ViewController retained by closure
- Listeners / observers not removed on lifecycle events
- Static references to large objects
- Large bitmaps not recycled (Android)

### Detection

- iOS: Instruments → Leaks, Allocations, VM Tracker
- Android: LeakCanary, Profiler → Memory
- RN: Flipper memory plugin
- Flutter: DevTools Memory tab

### Images

- Downsample to display size, don't load full resolution
- Use `AVIF` / `HEIC` where supported
- Lazy-load off-screen images
- Reuse bitmap pools on Android

---

## 4. Battery

### Worst Offenders

- Continuous GPS
- Wi-Fi / cellular usage (especially partial uploads)
- Wake locks / background processing
- High-frequency accelerometer / sensors
- Screen-on time (bright content, continuous animation)

### Reductions

- Batch network requests
- Use `fused location provider` (Android) or significant-change location (iOS)
- Prefer silent push + on-demand sync over background polling
- Respect Doze mode (Android) and low-power mode (iOS)
- Cache aggressively -- fewer round-trips

### Measurement

- Android: Battery Historian, Profiler → Energy
- iOS: Instruments → Energy Log, Xcode Organizer → Energy reports

---

## 5. Network

### Latency Matters More Than Bandwidth

Mobile radio has a high wake-up cost. Fewer, larger requests beat many small ones.

### Techniques

- HTTP/2 or HTTP/3 (multiplexing, lower handshake cost)
- Brotli / gzip compression
- Persistent connections (don't close prematurely)
- Request collapsing (debounce rapid-fire calls)
- Cache-Control + ETag for conditional requests
- Offline-first with background sync
- Image CDN with device-aware sizing

### Retry Policy

- Exponential backoff with jitter
- Max retries: 3 for transient, 0 for auth / 4xx
- Circuit breaker for persistent failures
- Never retry idempotent-unsafe operations without an idempotency key

---

## 6. Bundle / App Size

### Matter Because

- Slower install = higher abandonment
- Play: > 150 MB requires expansion files
- App Store: cellular download limited to 200 MB (was 150 MB)
- Emerging markets: users monitor data usage closely

### Reductions

| Platform | Technique |
|---|---|
| Android | R8 / Proguard minification, App Bundle dynamic delivery |
| iOS | Bitcode off (deprecated), Asset Catalogs, App Thinning |
| RN | Hermes, ProGuard, split APKs, remove unused locales |
| Flutter | `--split-per-abi`, deferred components, tree shaking (automatic) |

Measure:
- Android Studio → APK Analyzer
- Xcode → Report Navigator → App Size
- `react-native-bundle-visualizer`

---

## 7. List Rendering

Long lists are where most mobile apps fall apart.

| Platform | Recommended |
|---|---|
| RN | `FlatList` with `keyExtractor`, `getItemLayout` when fixed height, `removeClippedSubviews` |
| Flutter | `ListView.builder` (lazy), `SliverList` for complex scrolls |
| iOS SwiftUI | `LazyVStack` / `LazyVGrid` |
| iOS UIKit | `UICollectionView` with diffable datasource |
| Android Compose | `LazyColumn` / `LazyRow` with stable keys |
| Android Views | `RecyclerView` with `DiffUtil` |

Principles:
- Stable keys for items (not index)
- Fixed heights where possible (better scroll metrics)
- Pre-compute expensive derived state
- Virtualize images (placeholder → actual)

---

## 8. Animations

- Animate transforms / opacity (GPU), avoid layout animations on long lists
- Flutter: use `AnimatedBuilder`, avoid rebuilding whole widget trees
- iOS: Core Animation vs SwiftUI animations -- SwiftUI great, but profile
- Android: Compose AnimatedVisibility, Transition, use `animateAsState` sparingly
- Respect system reduce-motion setting

---

## 9. Offline Storage

| Store | Use |
|---|---|
| Preferences / UserDefaults / DataStore | Small key-value (< 1KB each) |
| Keychain / EncryptedSharedPreferences | Secrets, tokens |
| SQLite (Room / Core Data / WatermelonDB / Drift) | Structured data, queries |
| MMKV | Extremely fast KV store (RN, Android) |
| File system | Binary blobs, cached images |
| Realm | Complex object graphs |

Don't misuse preferences for large datasets; the OS rewrites the whole file on every change.

---

## 10. Instrumentation

Ship with observability from day one:

- **Crashes**: Crashlytics, Sentry, Bugsnag
- **Performance**: Firebase Performance Monitoring, Sentry Performance, Datadog RUM Mobile
- **Custom traces**: key user flows (checkout, sign-in)
- **Network**: sampled request timing
- **Analytics**: event naming convention shared across platforms

Watch these after every release -- regressions often appear only in production.

---

## 11. Performance Checklist

### Before each release

- [ ] Cold start measured on median device; < 2s
- [ ] No frame drops > 50% on typical user flows
- [ ] No memory leaks detected in Leaks / LeakCanary
- [ ] Battery impact acceptable in Energy Log
- [ ] Network retries + offline states work
- [ ] App size regression < 5% vs last release
- [ ] Long lists virtualized with stable keys
- [ ] Crash-free sessions > 99.5%
- [ ] Performance dashboard watched for 7 days post-release

---

## 12. Low-End Device Testing

Don't rely only on flagship devices. Test on:

- iOS: iPhone SE 2nd gen (A13), oldest supported iOS version
- Android: 4GB RAM, Snapdragon 6xx class, Android (min SDK) device

If it runs smooth there, it runs smooth everywhere.
