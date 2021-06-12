CREATE OR REPLACE FUNCTION bytea_import(p_path text, p_result OUT bytea)
LANGUAGE plpgsql AS $$
DECLARE
l_oid oid;
BEGIN
SELECT lo_import(p_path) INTO l_oid;
SELECT lo_get(l_oid) INTO p_result;
PERFORM lo_unlink(l_oid);
END;$$;

CREATE OR REPLACE FUNCTION "Create tables"()
    RETURNS void
    LANGUAGE 'sql'


AS $BODY$ CREATE TABLE IF NOT EXISTS public."Cards2"
(
    "id" integer NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
	"Image" bytea DEFAULT bytea_import('C:\magic\default.png'),
    "Name" character varying(50) COLLATE pg_catalog."default",
    "Card set" character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT "Cards2_pkey" PRIMARY KEY ("id")
);

CREATE INDEX IF NOT EXISTS Name ON "Cards2" ("Name");

CREATE TABLE IF NOT EXISTS public."FindInShops2"
(
    "id" integer NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
	"Set Name" character varying(50) COLLATE pg_catalog."default",
    "Shop Name" character varying(50) COLLATE pg_catalog."default",
    "Original set price" integer NOT NULL,
	"Creation time" timestamptz DEFAULT CURRENT_TIMESTAMP,
    "Last modified" timestamptz,
    CONSTRAINT "Shops2_pkey" PRIMARY KEY ("Set Name", "Shop Name")
);

INSERT INTO "Cards2" ("id", "Image", "Name", "Card set")
VALUES(001, bytea_import('magic\core21\en_wp7nVUSafb.png'), 'Daybreak Charger', 'Core Set 21'),
		(002, bytea_import('magic\ikoria\en_PjLvkLzdSQ.png'), 'Mothra, Supersonic Queen', 'Ikoria'),
		(003, bytea_import('magic\kaldheim\ru_sUrnxuYUqY.png'), 'Финн, Клыконосец', 'Калдхайм'),
		(004, bytea_import('magic\strixhaven\ru_upAklHKLFj.png'), 'Искривление Времени', 'Стриксхейвен'),
		(005, bytea_import('magic\ikoria\en_wgwxf71dPn.png'), 'Tentative Connection', 'Ikoria'),
		(006, bytea_import('magic\kaldheim\ru_gFjNFLjPld.png'), 'Карфеллский Псарь', 'Калдхайм'),
		(007, bytea_import('magic\kaldheim\ru_IDOYVhbin1.png'), 'Стражник Зала Богов', 'Калдхайм'),
		(008, bytea_import('magic\ikoria\en_T4HOiGr7fx.png'), 'Avian Oddity', 'Ikoria'),
		(009, bytea_import('magic\kaldheim\ru_ULWbffIYbH.png'), 'Ледошкурый Тролль', 'Калдхайм'),
		(010, bytea_import('magic\kaldheim\ru_wwAXaaL4oW.png'), 'Дракон Золотого Моста', 'Калдхайм'),
		(011, bytea_import('magic\core21\c.png'), 'Turret Ogre', 'Core Set 21'),
		(012, bytea_import('magic\strixhaven\ru_dLmhxxX9Xi.png'), 'Удар Молнии', 'Стриксхейвен'),
		(013, bytea_import('magic\core21\en_ztfyCQysLg.png'), 'Island', 'Core Set 21'),
		(014, bytea_import('magic\ikoria\en_U5Qg8aJtjf.png'), 'Suffocating Fumes', 'Ikoria'),
		(015, bytea_import('magic\strixhaven\ru_VoOTzlGkF7.png'), 'Выбор', 'Стриксхейвен'),
		(016, bytea_import('magic\core21\en_54KptLxJ1h.png'), 'Grim Tutor', 'Core Set 21'),
		(017, bytea_import('magic\strixhaven\ru_86MtC0M2SH.png'), 'Насилие', 'Стриксхейвен'),
		(018, bytea_import('magic\core21\en_fU3MEi77xk.png'), 'Feline Sovereign', 'Core Set 21'),
		(019, bytea_import('magic\ikoria\en_2bFeo99omt.png'), 'Lead the Stampede', 'Ikoria'),
		(020, bytea_import('magic\strixhaven\ru_GvGcna4vRF.png'), 'Мечи на Орала', 'Стриксхейвен');

INSERT INTO "FindInShops2" ("id", "Set Name", "Shop Name", "Original set price")
VALUES (001, 'Ikoria', 'Hobby Games', 2100),
		(002, 'Core21', 'Hobby Games', 1990),
		(003, 'Ikoria', 'Citadel', 2080),
		(004, 'Kaldheim', '20Graney', 2000),
		(005, 'Strixhaven', 'Hobby Games', 1990),
		(006, 'Ikoria', '20Graney', 2200),
		(007, 'Core21', 'Citadel', 1900);$BODY$;

CREATE OR REPLACE FUNCTION modification_time()
RETURNS TRIGGER AS $$
BEGIN
   NEW."Last modified" = CURRENT_TIMESTAMP;
   RETURN NEW;
END;
$$ language 'plpgsql';


DROP TRIGGER IF EXISTS updatetime on "FindInShops2";

CREATE TRIGGER updatetime BEFORE UPDATE
    ON "FindInShops2" FOR EACH ROW EXECUTE PROCEDURE 
    modification_time();

SELECT * FROM "FindInShops2";

CREATE OR REPLACE FUNCTION addCard(IN name character varying(50), IN set_ character varying(50)):
	RETURNS void
    LANGUAGE 'sql'
    
AS $BODY$ INSERT INTO "Cards2"("Name", "Card set")
	VALUES (name, set_);$BODY$;
        
CREATE OR REPLACE FUNCTION addShop(IN shop character varying(50), IN set_ character varying(50), IN cost integer):
    RETURNS void
    LANGUAGE 'sql'
    
AS $BODY$ INSERT INTO "FindInShops2"("Set Name", "Shop Name", "Original set price")
	VALUES (set_, shop, cost);$BODY$;

CREATE OR REPLACE FUNCTION clearCards():
	RETURNS void AS
	$$
	BEGIN
	  TRUNCATE "Cards2";
	END
	$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION clearShops():
	RETURNS void AS
	$$
	BEGIN
	  TRUNCATE "FindInShops2";
	END
	$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION clearAll():
	RETURNS void AS
	$$
	BEGIN
	  TRUNCATE "Cards2";
	  TRUNCATE "FindInShops2";
	END
	$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION search(IN key character varying(50)):
	RETURNS JSON AS
	$$
	BEGIN
	  RETURN (SELECT json_agg(json_build_object(
	  'Name', "Cards2"."Name",
	  'Card set', "Cards2"."Card set"
	  )) FROM "Cards2" WHERE "Cards2"."Name" LIKE CONCAT('%', key, '%'));
	END
	$$ LANGUAGE plpgsql;
	
CREATE OR REPLACE FUNCTION searchInShop(IN key character varying(50)):
	RETURNS JSON AS
	$$
	BEGIN
	  RETURN (SELECT json_agg(json_build_object(
	  'Shop name', "FindInShops2"."Shop name",
	  'Set name', "FindInShops2"."Set name"
	  )) FROM "FindInShops2" WHERE "FindInShops2"."Shop name" LIKE CONCAT('%', key, '%'));
	END
	$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION getCards():
	RETURNS JSON AS
	$$
	BEGIN
	  RETURN (SELECT json_agg(json_build_object(
	  'Name', "Cards2"."Name",
	  'Card set', "Cards2"."Card set",
	  'Image', "Cards2"."Image"
	  )) FROM "Cards2");
	END
	$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION getShops():
	RETURNS JSON AS
	$$
	BEGIN
	  RETURN (SELECT json_agg(json_build_object(
	  'Set Name', "FindInShops2"."Set Name",
	  'Shop Name', "FindInShops2"."Shop Name",
	  'Original set price', "FindInShops2"."Original set price",
	  'Creation time', "FindInShops2"."Creation time",
	  'Last modified', "FindInShops2"."Last modified"
	  )) FROM "FindInShops2");
	END
	$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION updateName(IN id integer, IN name character varying(50)):
	RETURNS void AS
	$$
	BEGIN
		UPDATE "Cards2" SET "Name" = name WHERE "Cards2"."id" = id;
	END
	$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION updateCardSet(IN id integer, IN set_ character varying(50)):
	RETURNS void AS
	$$
	BEGIN
		UPDATE "Cards2" SET "Card set" = set_ WHERE "Cards2"."id" = id;
	END
	$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION updateShop(IN id integer, IN shop character varying(50)):
	RETURNS void AS
	$$
	BEGIN
		UPDATE "FindInShops2" SET "Shop name" = shop WHERE "FindInShops2"."id" = id;
	END
	$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION updateShopSet(IN id integer, IN set_ character varying(50)):
	RETURNS void AS
	$$
	BEGIN
		UPDATE "FindInShops2" SET "Set name" = set_ WHERE "FindInShops2"."id" = id;
	END
	$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION updateCost(IN id integer, IN cost integer):
	RETURNS void AS
	$$
	BEGIN
		UPDATE "FindInShops2" SET "Original set price" = cost WHERE "FindInShops2"."id" = id;
	END
	$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION deleteCardByName(IN name character varying(50)):
	RETURNS void AS
	$$
	BEGIN
		DELETE FROM "Cards2" WHERE "Cards2"."Name" = name;
	END
	$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION deleteShopByName(IN shop character varying(50)):
	RETURNS void AS
	$$
	BEGIN
		DELETE FROM "FindInShops2" WHERE "FindInShops2"."Shop name" = shop;
	END
	$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION deleteCard(IN id integer):
	RETURNS void AS
	$$
	BEGIN
		DELETE FROM "Cards2" WHERE "Cards2"."id" = id;
	END
	$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION deleteShop(IN id integer):
	RETURNS void AS
	$$
	BEGIN
		DELETE FROM "FindInShops2" WHERE "FindInShops2"."id" = id;
	END
	$$ LANGUAGE plpgsql;

