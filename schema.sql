CREATE TABLE  IF NOT EXISTS contacts (
	contact_id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE,
	phone TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS groups (
   group_id INTEGER PRIMARY KEY,
   name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS contact_groups(
   contact_id INTEGER,
   group_id INTEGER,
   PRIMARY KEY (contact_id, group_id),
   FOREIGN KEY (contact_id) 
      REFERENCES contacts (contact_id) 
         ON DELETE CASCADE 
         ON UPDATE NO ACTION,
   FOREIGN KEY (group_id) 
      REFERENCES groups (group_id) 
         ON DELETE CASCADE 
         ON UPDATE NO ACTION
);
INSERT OR IGNORE INTO contacts (contact_id, first_name, last_name, email, phone)
VALUES( '1', 'anonyme', 'noname', 'anonymous@email.fr', '+2653546434');
INSERT OR IGNORE INTO contacts (contact_id, first_name, last_name, email, phone)
VALUES( '2', 'anne onim', 'onim', 'anne.onim@email.com', '+86877779898');
create table if not exists piece(
        id integer primary key autoincrement,
        name text,
            composer_artist text,
            time_signature text,
            key_signature text
      , created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP                );
create table if not exists bow_logic(
        id integer primary key autoincrement,
        position_de_depart text,
            longueur_archet text,
            duree_de_note text,
            pic text,
            time_signature text,
            key_signature text,
            tempo text,
            vitesse_archet text,
            nuances text,
            corde text,
            distance_chevalet text,
            position_manche text,
            description text
      , created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP                );
