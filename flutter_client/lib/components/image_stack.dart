import 'package:flutter/material.dart';
import 'package:transparent_image/transparent_image.dart';

class RecipeImage extends StatelessWidget {
  const RecipeImage({Key? key, required this.cdnUrl}) : super(key: key);
  final String? cdnUrl;

  _getImage(BuildContext context, String? cdnUrl) {
    if (cdnUrl == null || cdnUrl.isEmpty) {
      return Stack(children: <Widget>[
        Center(
            child: Ink.image(
          image: const AssetImage('assets/images/bread_placeholder.jpeg'),
          fit: BoxFit.cover,
        ))
      ]);
    } else {
      final FadeInImage breadImage = FadeInImage.memoryNetwork(
        placeholder: kTransparentImage,
        image: cdnUrl,
        fit: BoxFit.cover,
      );

      return Stack(
        children: <Widget>[
          const Center(child: CircularProgressIndicator()),
          SizedBox(
            width: MediaQuery.of(context).size.width,
            height: MediaQuery.of(context).size.height,
            child: breadImage,
          )
        ],
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: _getImage(context, cdnUrl),
    );
  }
}
