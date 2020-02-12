-- ----------------------------
-- Table structure for t_at_qqxx
-- ----------------------------
DROP TABLE IF EXISTS "db_apitesting"."t_at_qqxx";
CREATE TABLE "db_apitesting"."t_at_qqxx" (
  "c_bh" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "c_bh_zx" varchar(32) COLLATE "pg_catalog"."default",
  "n_xh" int4,
  "n_qqmc" varchar(255) COLLATE "pg_catalog"."default",
  "c_qqdz" varchar(255) COLLATE "pg_catalog"."default",
  "c_xysj" varchar(255) COLLATE "pg_catalog"."default",
  "dt_zxsj" timestamp(6),
  "n_jkzt" varchar(255) COLLATE "pg_catalog"."default",
  "c_yzjg" varchar(255) COLLATE "pg_catalog"."default",
  "c_qqcs" varchar(20000) COLLATE "pg_catalog"."default",
  "c_yqfhz" varchar(20000) COLLATE "pg_catalog"."default",
  "c_sjfhz" varchar(20000) COLLATE "pg_catalog"."default",
  "c_bh_yl" varchar(32) COLLATE "pg_catalog"."default",
  "c_xylx" varchar(255) COLLATE "pg_catalog"."default",
  "c_matchinfo" varchar(200000) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_bh" IS '请求编号';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_bh_zx" IS '执行编号';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."n_xh" IS '执行序号';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."n_qqmc" IS '请求名称';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_qqdz" IS '请求地址';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_xysj" IS '响应时间';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."dt_zxsj" IS '执行时间';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."n_jkzt" IS '接口返回状态';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_yzjg" IS '验证结果';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_qqcs" IS '请求参数';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_yqfhz" IS '预期返回值';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_sjfhz" IS '实际返回值';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_bh_yl" IS '用例编号';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_xylx" IS '协议类型';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_matchinfo" IS '校验信息';

-- ----------------------------
-- Table structure for t_at_xmxx
-- ----------------------------
DROP TABLE IF EXISTS "db_apitesting"."t_at_xmxx";
CREATE TABLE "db_apitesting"."t_at_xmxx" (
  "c_bh" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "c_xmmc" varchar(300) COLLATE "pg_catalog"."default",
  "c_url" varchar(500) COLLATE "pg_catalog"."default" NOT NULL,
  "dt_zxscsj" timestamp(6),
  "dt_zxzxsj" timestamp(6),
  "c_zxtgl" numeric(7,2),
  "c_zxfgl" numeric(7,2)
)
;
COMMENT ON COLUMN "db_apitesting"."t_at_xmxx"."c_bh" IS '项目编号';
COMMENT ON COLUMN "db_apitesting"."t_at_xmxx"."c_xmmc" IS '项目名称';
COMMENT ON COLUMN "db_apitesting"."t_at_xmxx"."c_url" IS '项目根地址';
COMMENT ON COLUMN "db_apitesting"."t_at_xmxx"."dt_zxscsj" IS '最新上传时间';
COMMENT ON COLUMN "db_apitesting"."t_at_xmxx"."dt_zxzxsj" IS '最新执行时间';
COMMENT ON COLUMN "db_apitesting"."t_at_xmxx"."c_zxtgl" IS '最新通过率';
COMMENT ON COLUMN "db_apitesting"."t_at_xmxx"."c_zxfgl" IS '最新覆盖率';

-- ----------------------------
-- Table structure for t_at_ylxx
-- ----------------------------
DROP TABLE IF EXISTS "db_apitesting"."t_at_ylxx";
CREATE TABLE "db_apitesting"."t_at_ylxx" (
  "c_bh" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "c_bh_xm" varchar(32) COLLATE "pg_catalog"."default",
  "c_ylmc" varchar(255) COLLATE "pg_catalog"."default",
  "dt_scsj" timestamp(6),
  "dt_zxzxsj" timestamp(6),
  "n_zxcs" int4,
  "c_bclj" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."c_bh" IS '用例编号';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."c_bh_xm" IS '项目编号';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."c_ylmc" IS '用例名称';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."dt_scsj" IS '上传时间';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."dt_zxzxsj" IS '最新执行时间';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."n_zxcs" IS '执行次数';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."c_bclj" IS '保存路径';

-- ----------------------------
-- Table structure for t_at_zxcs
-- ----------------------------
DROP TABLE IF EXISTS "db_apitesting"."t_at_zxcs";
CREATE TABLE "db_apitesting"."t_at_zxcs" (
  "c_bh" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "c_bh_yl" varchar(32) COLLATE "pg_catalog"."default",
  "c_key" varchar(255) COLLATE "pg_catalog"."default",
  "c_value" varchar(5000) COLLATE "pg_catalog"."default",
  "n_xh" int4
)
;
COMMENT ON COLUMN "db_apitesting"."t_at_zxcs"."c_bh" IS '执行参数的主键';
COMMENT ON COLUMN "db_apitesting"."t_at_zxcs"."c_bh_yl" IS '执行参数所属用例的编号';
COMMENT ON COLUMN "db_apitesting"."t_at_zxcs"."c_key" IS '执行参数的名称';
COMMENT ON COLUMN "db_apitesting"."t_at_zxcs"."c_value" IS '执行参数的内容';
COMMENT ON COLUMN "db_apitesting"."t_at_zxcs"."n_xh" IS '参数的序号，用来展示时排序的';

-- ----------------------------
-- Table structure for t_at_zxxx
-- ----------------------------
DROP TABLE IF EXISTS "db_apitesting"."t_at_zxxx";
CREATE TABLE "db_apitesting"."t_at_zxxx" (
  "c_bh" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "c_bh_yl" varchar(32) COLLATE "pg_catalog"."default",
  "dt_zxsj" timestamp(6),
  "c_fgl" numeric(7,2),
  "c_cgl" numeric(7,2),
  "c_tgl" numeric(7,2),
  "n_zt" varchar(255) COLLATE "pg_catalog"."default",
  "c_cg" varchar(8) COLLATE "pg_catalog"."default",
  "c_wcg" varchar(8) COLLATE "pg_catalog"."default",
  "c_tg" varchar(8) COLLATE "pg_catalog"."default",
  "c_wtg" varchar(8) COLLATE "pg_catalog"."default",
  "c_jd" numeric
)
;
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."c_bh" IS '执行编号';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."c_bh_yl" IS '用例编号';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."dt_zxsj" IS '执行时间';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."c_fgl" IS '覆盖率';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."c_cgl" IS '成功率';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."c_tgl" IS '通过率';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."n_zt" IS '执行状态（0：正在执行，1：已完成，2：已中断）';

-- ----------------------------
-- Primary Key structure for table t_at_qqxx
-- ----------------------------
ALTER TABLE "db_apitesting"."t_at_qqxx" ADD CONSTRAINT "t_at_qqxx_pkey" PRIMARY KEY ("c_bh");

-- ----------------------------
-- Primary Key structure for table t_at_xmxx
-- ----------------------------
ALTER TABLE "db_apitesting"."t_at_xmxx" ADD CONSTRAINT "t_at_xmxx_pkey" PRIMARY KEY ("c_bh", "c_url");

-- ----------------------------
-- Primary Key structure for table t_at_ylxx
-- ----------------------------
ALTER TABLE "db_apitesting"."t_at_ylxx" ADD CONSTRAINT "t_at_ylxx_pkey" PRIMARY KEY ("c_bh");

-- ----------------------------
-- Primary Key structure for table t_at_zxcs
-- ----------------------------
ALTER TABLE "db_apitesting"."t_at_zxcs" ADD CONSTRAINT "t_at_zxcs_pkey" PRIMARY KEY ("c_bh");

-- ----------------------------
-- Primary Key structure for table t_at_zxxx
-- ----------------------------
ALTER TABLE "db_apitesting"."t_at_zxxx" ADD CONSTRAINT "t_at_zxxx_pkey" PRIMARY KEY ("c_bh");
