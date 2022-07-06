class Step {
  final String name;
  final String description;
  final int id;
  final int durationInSeconds;

  const Step(
      {required this.name,
      required this.id,
      required this.description,
      required this.durationInSeconds});

  factory Step.fromJson(Map<String, dynamic> json) {
    return Step(
      name: json['name'],
      description: json['description'],
      id: json['id'],
      durationInSeconds: json['duration_in_seconds'],
    );
  }
}
