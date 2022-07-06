import 'package:baking_client/models/ingredient.dart';
import 'package:baking_client/models/step.dart';

class Procedure {
  final String name;
  final String description;
  final int id;
  final int order;
  final List<Ingredient> ingredients;
  final List<Step> steps;

  const Procedure(
      {required this.name,
      required this.id,
      required this.description,
      required this.order,
      required this.ingredients,
      required this.steps});

  factory Procedure.fromJson(Map<String, dynamic> json) {
    return Procedure(
      name: json['name'],
      description: json['description'],
      id: json['id'],
      order: json['order'],
      ingredients: (json['ingredients'] as List<dynamic>)
          .map((e) => Ingredient.fromJson(e as Map<String, dynamic>))
          .toList(),
      steps: (json['steps'] as List<dynamic>)
          .map((e) => Step.fromJson(e as Map<String, dynamic>))
          .toList(),
    );
  }
}
