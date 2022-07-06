import 'package:baking_client/models/procedure.dart';

class Recipe {
  final String name;
  final String description;
  final int id;
  final int hydration;
  final String? imageUrl;
  final String? cdnUrl;
  final List<Procedure> procedures;

  const Recipe(
      {required this.name,
      required this.id,
      required this.description,
      required this.imageUrl,
      required this.cdnUrl,
      required this.hydration,
      required this.procedures});

  factory Recipe.fromJson(Map<String, dynamic> json) {
    return Recipe(
      name: json['name'],
      description: json['description'],
      id: json['id'],
      hydration: json['hydration'],
      imageUrl: json['image_url'],
      cdnUrl: json['cdn_url'],
      procedures: (json['procedures'] as List<dynamic>)
          .map((e) => Procedure.fromJson(e as Map<String, dynamic>))
          .toList(),
    );
  }
}
