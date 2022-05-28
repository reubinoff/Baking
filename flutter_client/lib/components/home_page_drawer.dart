import 'package:flutter/material.dart';

class HomePageDrawer extends StatelessWidget {
  const HomePageDrawer({
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: Column(children: [
        Expanded(
            child: ListView(
          children: [
            const DrawerHeader(
              child: Text(
                'Baking',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                ),
              ),
              decoration: BoxDecoration(
                color: Colors.blueGrey,
              ),
            ),
            ListTile(
              leading: const Icon(Icons.person),
              title: const Text('Login'),
              onTap: () {
                Navigator.pop(context);
              },
            ),
            ListTile(
              leading: const Icon(Icons.favorite),
              title: const Text('Favorite'),
              onTap: () {
                Navigator.pop(context);
              },
            ),
          ],
        )),
        const Divider(
          height: 1,
          thickness: 1,
        ),
        const Padding(
          padding: EdgeInsets.all(16),
        ),
        ListTile(
          leading: const Icon(Icons.settings),
          title: const Text('Settings'),
          onTap: () {
            Navigator.pop(context);
          },
        ),
        ListTile(
          leading: const Icon(Icons.help),
          title: const Text('Help and Feedback'),
          onTap: () {
            Navigator.pop(context);
          },
        ),
        const Align(
          alignment: Alignment.bottomCenter,
          child: Text(
            'Made with ❤ by Moshe Reubinoff',
            style: TextStyle(
              color: Colors.grey,
              fontSize: 12,
            ),
          ),
        ),
      ]),
    );
  }
}
