import 'package:baking_client/models/recipe.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Baking app test', (WidgetTester tester) async {
    const Recipe r = Recipe(
      id: 1,
      description: 'test',
      name: 'name',
      hydration: 20,
      imageUrl: '',
      cdnUrl: '',
      procedures: [],
    );
    debugPrint(r.toString());
  });
}
