import 'package:flutter/foundation.dart';

class BakingUrl {
  final String baseDebugUrl = "localhost:8888";
  final String baseProdUrl = "service.baking.reubinoff.com";

  Uri createUrl(String unencodedPath, [Map<String, dynamic>? queryParameters]) {
    if (kDebugMode) {
      final url = Uri.http(baseDebugUrl, unencodedPath, queryParameters);
      debugPrint("BakingUrl: $url");
      return url;
    }
    return Uri.https(baseProdUrl, unencodedPath, queryParameters);
  }
}
