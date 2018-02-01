--
-- PostgreSQL database dump
--

-- Dumped from database version 10.1
-- Dumped by pg_dump version 10.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: hudou_area_seq; Type: SEQUENCE; Schema: public; Owner: hudou_user
--

CREATE SEQUENCE hudou_area_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE hudou_area_seq OWNER TO hudou_user;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: area; Type: TABLE; Schema: public; Owner: hudou_user
--

CREATE TABLE area (
    id integer DEFAULT nextval('hudou_area_seq'::regclass) NOT NULL,
    lid character varying(40) DEFAULT NULL::character varying,
    area_name character varying(20) DEFAULT NULL::character varying,
    long double precision,
    lat double precision,
    CONSTRAINT hudou_area_id_check CHECK ((id > 0))
);


ALTER TABLE area OWNER TO hudou_user;

--
-- Name: hudou_daliy_summary_seq; Type: SEQUENCE; Schema: public; Owner: hudou_user
--

CREATE SEQUENCE hudou_daliy_summary_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE hudou_daliy_summary_seq OWNER TO hudou_user;

--
-- Name: daily_summary; Type: TABLE; Schema: public; Owner: hudou_user
--

CREATE TABLE daily_summary (
    id integer DEFAULT nextval('hudou_daliy_summary_seq'::regclass) NOT NULL,
    total_rooms integer,
    sold_rooms integer,
    turnover real,
    date date NOT NULL,
    last_updated timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT hudou_daliy_summary_id_check CHECK ((id > 0)),
    CONSTRAINT hudou_daliy_summary_sold_rooms_check CHECK ((sold_rooms >= 0)),
    CONSTRAINT hudou_daliy_summary_total_rooms_check CHECK ((total_rooms >= 0))
);


ALTER TABLE daily_summary OWNER TO hudou_user;

--
-- Name: hudou_house_seq; Type: SEQUENCE; Schema: public; Owner: hudou_user
--

CREATE SEQUENCE hudou_house_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE hudou_house_seq OWNER TO hudou_user;

--
-- Name: house; Type: TABLE; Schema: public; Owner: hudou_user
--

CREATE TABLE house (
    id integer DEFAULT nextval('hudou_house_seq'::regclass) NOT NULL,
    uuid character varying(40) DEFAULT '0'::character varying NOT NULL,
    lid character varying(40) DEFAULT '0'::character varying NOT NULL,
    area_id integer,
    area_name character varying(30) DEFAULT NULL::character varying,
    title character varying(128) NOT NULL,
    price real DEFAULT '0'::real NOT NULL,
    lang double precision DEFAULT '0'::double precision NOT NULL,
    lat double precision DEFAULT '0'::double precision NOT NULL,
    model character varying(30) DEFAULT '0'::character varying NOT NULL,
    status smallint DEFAULT '0'::smallint NOT NULL,
    create_time timestamp(0) without time zone NOT NULL,
    last_updated timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT hudou_house_area_id_check CHECK ((area_id > 0)),
    CONSTRAINT hudou_house_id_check CHECK ((id > 0)),
    CONSTRAINT hudou_house_lang_check CHECK ((lang > (0)::double precision)),
    CONSTRAINT hudou_house_lat_check CHECK ((lat > (0)::double precision)),
    CONSTRAINT hudou_house_price_check CHECK ((price > (0)::real)),
    CONSTRAINT hudou_house_status_check CHECK ((status > 0))
);


ALTER TABLE house OWNER TO hudou_user;

--
-- Name: hudou_housesold_seq; Type: SEQUENCE; Schema: public; Owner: hudou_user
--

CREATE SEQUENCE hudou_housesold_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE hudou_housesold_seq OWNER TO hudou_user;

--
-- Name: house_sold; Type: TABLE; Schema: public; Owner: hudou_user
--

CREATE TABLE house_sold (
    id integer DEFAULT nextval('hudou_housesold_seq'::regclass) NOT NULL,
    house_id integer,
    price real,
    special_price real,
    date date,
    status smallint,
    last_updated timestamp(0) without time zone DEFAULT NULL::timestamp without time zone,
    CONSTRAINT hudou_housesold_house_id_check CHECK ((house_id > 0)),
    CONSTRAINT hudou_housesold_id_check CHECK ((id > 0)),
    CONSTRAINT hudou_housesold_price_check CHECK ((price >= (0)::real)),
    CONSTRAINT hudou_housesold_special_price_check CHECK ((special_price >= (0)::real))
);


ALTER TABLE house_sold OWNER TO hudou_user;

--
-- Name: hudou_area_seq; Type: SEQUENCE SET; Schema: public; Owner: hudou_user
--

SELECT pg_catalog.setval('hudou_area_seq', 5, false);


--
-- Name: hudou_daliy_summary_seq; Type: SEQUENCE SET; Schema: public; Owner: hudou_user
--

SELECT pg_catalog.setval('hudou_daliy_summary_seq', 43, true);


--
-- Name: hudou_house_seq; Type: SEQUENCE SET; Schema: public; Owner: hudou_user
--

SELECT pg_catalog.setval('hudou_house_seq', 68, false);


--
-- Name: hudou_housesold_seq; Type: SEQUENCE SET; Schema: public; Owner: hudou_user
--

SELECT pg_catalog.setval('hudou_housesold_seq', 915, true);


--
-- Name: area hudou_area_pkey; Type: CONSTRAINT; Schema: public; Owner: hudou_user
--

ALTER TABLE ONLY area
    ADD CONSTRAINT hudou_area_pkey PRIMARY KEY (id);


--
-- Name: daily_summary hudou_daliy_summary_pkey; Type: CONSTRAINT; Schema: public; Owner: hudou_user
--

ALTER TABLE ONLY daily_summary
    ADD CONSTRAINT hudou_daliy_summary_pkey PRIMARY KEY (id);


--
-- Name: house hudou_house_pkey; Type: CONSTRAINT; Schema: public; Owner: hudou_user
--

ALTER TABLE ONLY house
    ADD CONSTRAINT hudou_house_pkey PRIMARY KEY (id);


--
-- Name: house_sold hudou_housesold_pkey; Type: CONSTRAINT; Schema: public; Owner: hudou_user
--

ALTER TABLE ONLY house_sold
    ADD CONSTRAINT hudou_housesold_pkey PRIMARY KEY (id);


--
-- Name: daily_summary unq_date; Type: CONSTRAINT; Schema: public; Owner: hudou_user
--

ALTER TABLE ONLY daily_summary
    ADD CONSTRAINT unq_date UNIQUE (date);


--
-- Name: house_sold unq_house_id_date; Type: CONSTRAINT; Schema: public; Owner: hudou_user
--

ALTER TABLE ONLY house_sold
    ADD CONSTRAINT unq_house_id_date UNIQUE (house_id, date);


--
-- Name: area unq_lid; Type: CONSTRAINT; Schema: public; Owner: hudou_user
--

ALTER TABLE ONLY area
    ADD CONSTRAINT unq_lid UNIQUE (lid);


--
-- Name: house unq_uuid; Type: CONSTRAINT; Schema: public; Owner: hudou_user
--

ALTER TABLE ONLY house
    ADD CONSTRAINT unq_uuid UNIQUE (uuid);


--
-- Name: PRI_ID; Type: INDEX; Schema: public; Owner: hudou_user
--

CREATE INDEX "PRI_ID" ON daily_summary USING btree (id);


--
-- PostgreSQL database dump complete
--

