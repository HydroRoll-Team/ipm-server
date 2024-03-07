<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:template match="/ipm_package_data">
        <HTML>
            <HEAD>
                <TITLE>IPM PACKAGE SERVER</TITLE>
            </HEAD>
            <BODY bgcolor="white" text="navy">
                <H1>INFINI RULE PACKAGES</H1>
                <P>IPM has built-in support for dozens of packages and collections, as listed below.
        To use these within IPM/INFINI we recommend that you use the IPM <TT>&gt;&gt;&gt;
                        ipm add</TT> command.</P>
                <P>Please consult the README file included with each
                    packages for further information.</P>
                <OL>
                    <xsl:for-each select="//packages/package">
                        <LI><I>
                                <xsl:value-of select="@name" />
                            </I> [<a
                                href="https://ipm.hydroroll.team{substring-after(@url, 'https://raw.githubusercontent.com/HydroRoll-Team/ipm-server/gh-pages')}">
        download </a> |<a href="{@webpage}">
                                source </a>] <BR /> id: <tt>
                                <xsl:value-of select="@id" />
                            </tt>;
        size: <xsl:value-of select="@size" />; author: <xsl:value-of select="@author" />; copyright: <xsl:value-of
                                select="@copyright" />; license: <xsl:value-of select="@license" />; <P />
                        </LI>
                    </xsl:for-each>
                </OL>
                <HR />
                <A href="http://ipm.hydroroll.team/index">IPM PACKAGE SERVER</A>
            </BODY>
        </HTML>
    </xsl:template>
</xsl:stylesheet>